# Arquivo: app.py (ATUALIZADO PARA API 5 DIAS / 3 HORAS)
from flask import Flask, request, jsonify
import joblib
import pandas as pd
import numpy as np
import tensorflow as tf
import warnings
from flask_cors import CORS
import requests
from datetime import datetime

# --- SUA CHAVE DE API ESTA AQUI ---
API_KEY = "cbb8e8b6c4d5793c5e634985d25e720e"
# ---------------------------------

warnings.filterwarnings("ignore", message=".*HDF5 file format is considered legacy.*")

# --- 1. Carregamento (Sem mudanca) ---
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
    print(f"Base de Conhecimento (clima_cidades.csv) carregada com {len(KB_CLIMA)} cidades.")
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

# (MODULOS 1 e 2: validar_janela_plantio e get_risk_explanation - SEM MUDANCAS)
def validar_janela_plantio(mes):
    meses_validos_ml = ['Setembro', 'Outubro', 'Novembro', 'Dezembro']
    if mes in meses_validos_ml: return {'status': 'VALIDO_PARA_ML'}
    if mes in ['Junho', 'Julho', 'Agosto']:
        return {'status': 'INVIAVEL', 'risco': 'Inviavel', 'explicacao': {'titulo': 'Vazio Sanitario', 'detalhe': 'Este e o periodo do Vazio Sanitario, estabelecido por lei. Plantar soja e proibido para quebrar o ciclo do fungo da ferrugem-asiatica, que nao sobrevive sem a planta viva.', 'solucao': 'Aguarde o fim do Vazio Sanitario e o inicio oficial da janela de plantio (geralmente em Setembro).'}}
    if mes in ['Marco', 'Abril', 'Maio']:
        return {'status': 'INVIAVEL', 'risco': 'Inviavel', 'explicacao': {'titulo': 'Epoca de Colheita', 'detalhe': 'Este mes corresponde a epoca de colheita da safra principal. O solo e o clima (menos chuva) nao sao adequados para iniciar um novo plantio.', 'solucao': 'O plantio e agronomicamente inviavel. Conclua a colheita e inicie o planejamento da proxima safra (Set-Dez).'}}
    if mes in ['Janeiro', 'Fevereiro']:
        return {'status': 'INVIAVEL', 'risco': 'Inviavel', 'explicacao': {'titulo': 'Risco de Pragas e Doencas', 'detalhe': 'Plantar tao tarde (sementeira tardia) expoe a lavoura a um risco extremo de pragas (como percevejos) e doencas, alem de estresse hidrico no fim do ciclo.', 'solucao': 'O risco de perda total e altissimo. E fortemente recomendado nao plantar. Conclua a safra atual e aguarde Setembro.'}}
    return {'status': 'INVIAVEL', 'risco': 'Inviavel', 'explicacao': {'titulo': 'Erro', 'detalhe': 'Mes desconhecido.', 'solucao': 'Selecione um mes valido.'}}

def get_risk_explanation(temp, precip, geada, mes):
    if geada == 'Alto' and mes == 'Setembro': return {'titulo': 'Risco de Geada Tardia', 'detalhe': f'Risco "Alto". A media historica ({geada}) indica perigo de geadas tardias em {mes}. A geada pode **queimar e matar as plantulas** recem-emergidas, causando perda total.', 'solucao': 'NAO PLANTE AGORA. Recomenda-se fortemente **aguardar** o proximo mes (Outubro), quando o risco de geada diminui drasticamente.'}
    if geada == 'Medio' and mes == 'Setembro' or (geada == 'Alto' and mes == 'Outubro'): return {'titulo': 'Risco de Geada Moderado', 'detalhe': f'Risco "Medio". Embora menos provavel, uma geada tardia ainda pode ocorrer e causar **danos severos** as plantulas.', 'solucao': 'Se decidir plantar, utilize cultivares mais tolerantes ao frio e faca um seguro. O mais seguro e aguardar 15-20 dias.'}
    if precip < 1300 and mes == 'Dezembro': return {'titulo': 'Risco de Estresse Hidrico (Seca)', 'detalhe': f'Risco "Alto". A combinacao de baixa chuva ({precip}mm) com o calor de {mes} pode causar um "veranico", **impedindo o enchimento dos graos**.', 'solucao': 'Plantio nao recomendado sem sistema de irrigacao. Se possivel, antecipe para Outubro/Novembro, ou use cultivares muito resistentes a seca.'}
    if precip < 1400: return {'titulo': 'Risco de Chuva Irregular', 'detalhe': f'Risco "Medio". A media de {precip}mm esta abaixo do ideal (1400mm+). A falta de chuva pode **atrasar o desenvolvimento** inicial da planta.', 'solucao': 'Monitore as previsoes de chuva de curto prazo. Garanta um bom manejo do solo (ex: plantio direto) para reter umidade.'}
    if temp > 28: return {'titulo': 'Risco de Calor Excessivo', 'detalhe': f'Risco "Medio". A media de {temp}C esta acima de 28C. O calor excessivo pode causar o **abortamento de flores**, reduzindo drasticamente a produtividade.', 'solucao': 'Escolha cultivares de ciclo adaptado a regioes quentes, que sejam geneticamente mais tolerantes ao calor.'}
    if geada == 'Baixo' and (temp >= 22 and temp <= 27) and precip > 1500 and mes in ['Outubro', 'Novembro']: return {'titulo': 'Condicoes Ideais', 'detalhe': f'Risco "Baixo". A relacao entre temperatura ({temp}C), chuva ({precip}mm) e baixo risco de geada e **excelente** para a germinacao e desenvolvimento da soja.', 'solucao': 'Janela ideal. Prossiga com o plantio seguindo as boas praticas (ex: tratamento de semente, adubacao correta).'}
    if mes in ['Outubro', 'Novembro']: return {'titulo': 'Condicoes Favoraveis', 'detalhe': f'Risco "Baixo". Os dados historicos de temperatura ({temp}C) e chuva ({precip}mm) indicam uma boa janela para o plantio, livre dos principais riscos climaticos.', 'solucao': 'Janela recomendada. Prossiga com o planejamento.'}
    return {'titulo': 'Condicoes de Inicio/Fim de Safra', 'detalhe': 'Risco "Medio". Os dados climaticos estao dentro da media, mas por estar no inicio (Set) ou fim (Dez) da janela, ha riscos leves.', 'solucao': 'Plantio viavel, mas exige monitoramento. Se for Setembro, atencao a geada. Se for Dezembro, atencao a veranicos.'}


@app.route('/predict', methods=['POST'])
def predict():
    # (O endpoint /predict nao muda)
    prediction_label = None
    prob_dict = None
    explicacao_ml = None
    input_data = {}
    data = request.get_json()
    if not data: return jsonify({'erro': 'Nenhum dado JSON recebido.'}), 400
    try:
        user_cidade = data['cidade']
        user_estado = data['estado']
        user_janela = data['janela_plantio']
        input_data = data.copy()
    except KeyError as e:
        return jsonify({'erro': f'Campo obrigatorio ausente no JSON: {e}.'}), 400
    if not all([model, preprocessor, label_encoder, KB_CLIMA is not None]):
        return jsonify({'erro': 'Modelos ou Base de Clima nao estao carregados.'}), 500
    try:
        validacao = validar_janela_plantio(user_janela)
        if validacao['status'] == 'INVIAVEL':
            response = {'risco_plantio_previsto': validacao['risco'], 'probabilidades': {'Inviavel': 1.0}, 'explicacao': validacao['explicacao'], 'dados_utilizados': input_data}
            return jsonify(response)
        climate_data = get_climate_data(user_cidade)
        if climate_data is None:
            return jsonify({'erro': f'Dados climaticos nao encontrados para a cidade: {user_cidade}'}), 404
        input_data.update(climate_data)
        input_df = pd.DataFrame([input_data])
        X_processed = preprocessor.transform(input_df)
        probabilidades = model.predict(X_processed, verbose=0)[0] 
        prediction_index = np.argmax(probabilidades)
        prediction_label = label_encoder.inverse_transform([prediction_index])[0]
        prob_dict = {classe: float(prob) for classe, prob in zip(classes_alvo, probabilidades)}
        explicacao_ml = get_risk_explanation(input_data['temperatura_media'], input_data['precipitacao_media'], input_data['risco_geada'], input_data['janela_plantio'])
    except Exception as e:
        return jsonify({'erro': f'Erro durante o processamento: {e}'}), 500
    response = {'risco_plantio_previsto': prediction_label, 'probabilidades': prob_dict, 'explicacao': explicacao_ml, 'dados_utilizados': input_data }
    return jsonify(response)


# --- MUDANCA AQUI: ENDPOINT DE ANALISE TATICA (TEMPO) ---
@app.route('/get_weather_forecast', methods=['POST'])
def get_weather_forecast():
    if API_KEY == "COLE_SUA_CHAVE_API_KEY_AQUI":
        return jsonify({'erro': 'A chave da API OpenWeatherMap nao foi configurada no servidor.'}), 500

    data = request.get_json()
    cidade = data.get('cidade')
    
    local_data = get_climate_data(cidade)
    if not local_data:
        return jsonify({'erro': 'Cidade nao encontrada na base de dados interna.'}), 404
    
    lat = local_data.get('lat')
    lon = local_data.get('lon')

    try:
        # --- MUDANCA: URL DA API para "forecast" (5 dias / 3 horas) ---
        url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={API_KEY}&units=metric&lang=pt_br"
        response = requests.get(url)
        response.raise_for_status()
        weather_data = response.json()
    except requests.exceptions.HTTPError as err:
         if response.status_code == 401:
            return jsonify({'erro': 'Chave de API OpenWeatherMap invalida ou nao autorizada.'}), 401
         return jsonify({'erro': f'Erro ao chamar API de tempo: {err}'}), 500
    except Exception as e:
        return jsonify({'erro': f'Erro ao processar dados de tempo: {e}'}), 500

    # --- MUDANCA: LOGICA DE PROCESSAMENTO ---
    # A API "forecast" retorna uma 'list' de 40 items (8 por dia, de 3 em 3 horas)
    
    daily_forecasts = {} # Dicionario para agrupar por dia
    frost_risk = False
    rain_soon = False
    
    for forecast_block in weather_data['list']:
        # 1. Extrai dados do bloco de 3 horas
        timestamp = forecast_block['dt']
        data_dia_str = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')
        dia_label = datetime.fromtimestamp(timestamp).strftime('%d/%m')
        temp_min = forecast_block['main']['temp_min']
        temp_max = forecast_block['main']['temp_max']
        weather_desc = forecast_block['weather'][0]['description']

        # 2. Checa riscos taticos
        if temp_min < 3:
            frost_risk = True
        if 'chuva' in weather_desc.lower() and forecast_block.get('pop', 0) > 0.4:
            rain_soon = True
            
        # 3. Agrupa os dados por dia (para o grafico de linha)
        if data_dia_str not in daily_forecasts:
            daily_forecasts[data_dia_str] = {
                'dia': dia_label,
                'min': temp_min,
                'max': temp_max,
                'descs': {weather_desc}
            }
        else:
            # Atualiza o min/max do dia
            if temp_min < daily_forecasts[data_dia_str]['min']:
                daily_forecasts[data_dia_str]['min'] = temp_min
            if temp_max > daily_forecasts[data_dia_str]['max']:
                daily_forecasts[data_dia_str]['max'] = temp_max
            daily_forecasts[data_dia_str]['descs'].add(weather_desc)

    # 4. Converte o dicionario de volta para uma lista
    final_forecast_list = []
    for dia_data in daily_forecasts.values():
        final_forecast_list.append({
            'dia': dia_data['dia'],
            'min': dia_data['min'],
            'max': dia_data['max'],
            'desc': ', '.join(dia_data['descs'])
        })
            
    return jsonify({
        'forecast_list': final_forecast_list,
        'frost_risk_real': frost_risk,
        'rain_soon': rain_soon
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)