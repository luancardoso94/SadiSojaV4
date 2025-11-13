# Arquivo: gerar_dados_soja.py (ATUALIZADO PARA MESES)
import pandas as pd
import numpy as np

try:
    df_clima = pd.read_csv('clima_cidades.csv')
    print(f"Base de clima lida: {len(df_clima)} cidades encontradas.")
except FileNotFoundError:
    print("ERRO: 'clima_cidades.csv' nao encontrado.")
    print("Por favor, rode 'gerar_base_clima.py' primeiro.")
    exit()

# --- MUDANCA: Agora usamos meses individuais ---
# Estes sao os unicos meses que o ML vai aprender
janelas_plantio_validas = ['Setembro', 'Outubro', 'Novembro', 'Dezembro']

# --- MUDANCA: Regras mais finas por mes ---
def definir_risco_plantio(temp, precip, geada, mes):
    # Regra 1: Geada
    if geada == 'Alto' and mes == 'Setembro': return 'Alto'
    if geada == 'Alto' and mes == 'Outubro': return 'Medio'
    if geada == 'Medio' and mes == 'Setembro': return 'Medio'

    # Regra 2: Seca
    if precip < 1300 and mes == 'Dezembro': return 'Alto' # Dezembro e mais quente
    if precip < 1400: return 'Medio'

    # Regra 3: Calor
    if temp > 28: return 'Medio'

    # Regra 4: Ideal
    if geada == 'Baixo' and (temp >= 22 and temp <= 27) and precip > 1500 and mes in ['Outubro', 'Novembro']:
        return 'Baixo'
        
    if mes in ['Outubro', 'Novembro']: return 'Baixo'
    
    return 'Medio'

N_AMOSTRAS_TOTAL = len(df_clima) * 50
dados_finais = []

print(f"Gerando {N_AMOSTRAS_TOTAL} amostras de dados de treino (validos)...")

for _ in range(N_AMOSTRAS_TOTAL):
    perfil_row = df_clima.sample(1).iloc[0]
    perfil = perfil_row.to_dict()
    
    temp_final = round(perfil['temperatura_media'] + np.random.uniform(-1.5, 1.5), 1)
    precip_final = int(perfil['precipitacao_media'] + np.random.uniform(-100, 100))
    risco_geada_final = perfil['risco_geada']
    
    # --- MUDANCA: Escolhe um mes valido aleatorio ---
    janela_escolhida = np.random.choice(janelas_plantio_validas)
    
    risco_final = definir_risco_plantio(
        temp_final, precip_final, risco_geada_final, janela_escolhida
    )
    
    dados_finais.append({
        'estado': perfil['estado'],
        'cidade': perfil['cidade'],
        'temperatura_media': temp_final,
        'precipitacao_media': precip_final,
        'risco_geada': risco_geada_final,
        'janela_plantio': janela_escolhida, # O nome da coluna continua
        'risco_plantio': risco_final
    })

df = pd.DataFrame(dados_finais)
df = df.sample(frac=1).reset_index(drop=True)
nome_arquivo = 'dados_soja.csv'
df.to_csv(nome_arquivo, index=False)

print(f"Base de dados salva com sucesso em '{nome_arquivo}'!")