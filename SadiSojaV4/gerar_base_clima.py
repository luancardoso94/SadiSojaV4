# Arquivo: gerar_base_clima.py (SEM ACENTO)
import pandas as pd

print("Criando a Base de Conhecimento Climatologico (clima_cidades.csv)...")

perfis_climaticos = [
    # Rio Grande do Sul
    {'cidade': 'Passo Fundo', 'estado': 'RS', 'temperatura_media': 18.0, 'precipitacao_media': 1800, 'risco_geada': 'Alto'},
    {'cidade': 'Santa Maria', 'estado': 'RS', 'temperatura_media': 20.0, 'precipitacao_media': 1750, 'risco_geada': 'Medio'},
    {'cidade': 'Pelotas', 'estado': 'RS', 'temperatura_media': 19.0, 'precipitacao_media': 1600, 'risco_geada': 'Baixo'},
    {'cidade': 'Ijui', 'estado': 'RS', 'temperatura_media': 19.5, 'precipitacao_media': 1850, 'risco_geada': 'Medio'}, # Alterado

    # Santa Catarina
    {'cidade': 'Chapeco', 'estado': 'SC', 'temperatura_media': 20.0, 'precipitacao_media': 1900, 'risco_geada': 'Medio'},
    {'cidade': 'Lages', 'estado': 'SC', 'temperatura_media': 17.0, 'precipitacao_media': 1600, 'risco_geada': 'Alto'},
    {'cidade': 'Joacaba', 'estado': 'SC', 'temperatura_media': 18.5, 'precipitacao_media': 1700, 'risco_geada': 'Medio'},

    # Parana
    {'cidade': 'Londrina', 'estado': 'PR', 'temperatura_media': 23.0, 'precipitacao_media': 1600, 'risco_geada': 'Baixo'},
    {'cidade': 'Cascavel', 'estado': 'PR', 'temperatura_media': 22.0, 'precipitacao_media': 1700, 'risco_geada': 'Medio'},
    {'cidade': 'Ponta Grossa', 'estado': 'PR', 'temperatura_media': 19.5, 'precipitacao_media': 1550, 'risco_geada': 'Medio'},
    {'cidade': 'Guarapuava', 'estado': 'PR', 'temperatura_media': 18.0, 'precipitacao_media': 1650, 'risco_geada': 'Alto'},

    # Mato Grosso do Sul
    {'cidade': 'Dourados', 'estado': 'MS', 'temperatura_media': 24.0, 'precipitacao_media': 1500, 'risco_geada': 'Baixo'},
    {'cidade': 'Campo Grande', 'estado': 'MS', 'temperatura_media': 25.0, 'precipitacao_media': 1450, 'risco_geada': 'Baixo'},

    # Mato Grosso
    {'cidade': 'Sinop', 'estado': 'MT', 'temperatura_media': 27.0, 'precipitacao_media': 2000, 'risco_geada': 'Baixo'},
    {'cidade': 'Rondonopolis', 'estado': 'MT', 'temperatura_media': 26.0, 'precipitacao_media': 1400, 'risco_geada': 'Baixo'},
    {'cidade': 'Cuiaba', 'estado': 'MT', 'temperatura_media': 28.0, 'precipitacao_media': 1400, 'risco_geada': 'Baixo'},
    {'cidade': 'Sorriso', 'estado': 'MT', 'temperatura_media': 26.5, 'precipitacao_media': 1900, 'risco_geada': 'Baixo'},

    # Goias
    {'cidade': 'Rio Verde', 'estado': 'GO', 'temperatura_media': 25.0, 'precipitacao_media': 1700, 'risco_geada': 'Baixo'},
    {'cidade': 'Jatai', 'estado': 'GO', 'temperatura_media': 24.5, 'precipitacao_media': 1650, 'risco_geada': 'Baixo'},

    # Bahia
    {'cidade': 'Barreiras', 'estado': 'BA', 'temperatura_media': 26.0, 'precipitacao_media': 1300, 'risco_geada': 'Baixo'},
    {'cidade': 'Luis Eduardo Magalhaes', 'estado': 'BA', 'temperatura_media': 25.5, 'precipitacao_media': 1200, 'risco_geada': 'Baixo'}
]

df = pd.DataFrame(perfis_climaticos)
df.to_csv('clima_cidades.csv', index=False, encoding='utf-8')

print(f"Arquivo 'clima_cidades.csv' criado com {len(df)} cidades.")