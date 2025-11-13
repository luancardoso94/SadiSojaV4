# Arquivo: app.py (SISTEMA HIBRIDO)
from flask import Flask, request, jsonify
import joblib
import pandas as pd
import numpy as np
import tensorflow as tf
import warnings
from flask_cors import CORS

warnings.filterwarnings("ignore", message=".*HDF5 file format is considered legacy.*")

print("Carregando artefatos do modelo...")
KB_CLIMA = None
KB_MAPA_CIDADES = None
try:
    model = tf.keras.models.load_model('modelo_soja_tf.h5')
    preprocessor = joblib.load('preprocessor.pkl')
    label_encoder = joblib.load('label_encoder.pkl')
    classes_alvo = label_encoder.classes_
    print("Modelos de ML carregados!")

    df_clima_base = pd.read_csv('clima_cidades.csv')
    KB_CLIMA = df_clima_base.copy()
    KB_CLIMA.set_index('cidade', inplace=True)
    KB_MAPA_CIDADES = df_clima_base.groupby('estado')['cidade'].apply(list).to_dict()
    print(f"Base de Conhecimento carregada com {len(KB_CLIMA)} cidades.")
except Exception as e:
    print(f"ERRO CRITICO AO CARREGAR: {e}")
    model, preprocessor, label_encoder, classes_alvo = None, None, None, None

def get_climate_data(cidade):
    if KB_CLIMA is None: return None
    try:
        dados = KB_CLIMA.loc[cidade]
        return dados.to_dict()
    except KeyError:
        return None

app = Flask(__name__)
CORS(app) 

@app.route('/get_cidades', methods=['GET'])
def get_cidades():
    return jsonify(KB_MAPA_CIDADES)

# --- MODULO 1: O VALIDADOR (SISTEMA ESPECIALISTA) ---
def validar_janela_plantio(mes):
    """
    Este e o Modulo 1 (Baseado em Regras).
    Ele valida se o mes e agronomicamente viavel.
    """
    # Meses validos que o ML (Modulo 2) ira processar
    meses_validos_ml = ['Setembro', 'Outubro', 'Novembro', 'Dezembro']
    
    if mes in meses_validos_ml:
        return {'status': 'VALIDO_PARA_ML'}

    # Regras para meses inviaveis
    if mes in ['Junho', 'Julho', 'Agosto']:
        return {'status': 'INVIAVEL', 'risco': 'Inviavel (Vazio Sanitario)'}
    
    if mes in ['Marco', 'Abril', 'Maio']:
        return {'status': 'INVIAVEL', 'risco': 'Inviavel (Epoca de Colheita)'}

    if mes in ['Janeiro', 'Fevereiro']:
        return {'status': 'INVIAVEL', 'risco': 'Inviavel (Sementeira tardia / Risco de doencas)'}
        
    return {'status': 'INVIAVEL', 'risco': 'Mes desconhecido'}
# --- FIM DO MODULO 1 ---


@app.route('/predict', methods=['POST'])
def predict():
    if not all([model, preprocessor, label_encoder, KB_CLIMA is not None]):
        return jsonify({'erro': 'Modelos ou Base de Clima nao estao carregados.'}), 500

    data = request.get_json()
    if not data: return jsonify({'erro': 'Nenhum dado JSON recebido.'}), 400

    try:
        user_cidade = data['cidade']
        user_estado = data['estado']
        user_janela = data['janela_plantio'] # Agora sera 'Janeiro', 'Fevereiro', etc.
    except KeyError as e:
        return jsonify({'erro': f'Campo obrigatorio ausente no JSON: {e}.'}), 400

    try:
        # --- ETAPA 1: Rodar o Validador (Modulo 1) ---
        validacao = validar_janela_plantio(user_janela)
        
        if validacao['status'] == 'INVIAVEL':
            # Se for inviavel, nao usamos o ML. Retornamos a regra direto.
            response = {
                'risco_plantio_previsto': validacao['risco'],
                'probabilidades': {'Inviavel': 1.0}, # Probabilidade customizada
                'dados_utilizados': data
            }
            return jsonify(response)

        # --- ETAPA 2: Chamar a API de Clima (se necessario) ---
        climate_data = get_climate_data(user_cidade)
        if climate_data is None:
            return jsonify({'erro': f'Dados climaticos nao encontrados: {user_cidade}'}), 404

        # --- ETAPA 3: Rodar o Motor de IA (Modulo 2) ---
        input_data = {
            'estado': user_estado,
            'cidade': user_cidade,
            'janela_plantio': user_janela, # O ML foi treinado com 'Setembro', 'Outubro', etc.
            'temperatura_media': climate_data['temperatura_media'],
            'precipitacao_media': climate_data['precipitacao_media'],
            'risco_geada': climate_data['risco_geada']
        }

        input_df = pd.DataFrame([input_data])
        X_processed = preprocessor.transform(input_df)

        probabilidades = model.predict(X_processed, verbose=0)[0]
        prediction_index = np.argmax(probabilidades)
        prediction_label = label_encoder.inverse_transform([prediction_index])[0]
        
        prob_dict = {
            classe: float(prob) for classe, prob in zip(classes_alvo, probabilidades)
        }

    except Exception as e:
        return jsonify({'erro': f'Erro durante o processamento: {e}'}), 500

    response = {
        'risco_plantio_previsto': prediction_label,
        'probabilidades': prob_dict,
        'dados_utilizados': input_data 
    }
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True, port=5000)