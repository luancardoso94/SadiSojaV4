# Arquivo: gerar_base_clima.py (Versao CORRETA, com 21 cidades reais e Lat/Lon)
import pandas as pd
import numpy as np

print("Criando a Base de Conhecimento Climatologico (clima_cidades.csv)...")

# Esta e a nossa base de 21 cidades "reais" (nossas sementes)
perfis_base_reais = [
    {'cidade': 'Passo Fundo', 'estado': 'RS', 'lat': -28.26, 'lon': -52.40, 'temperatura_media': 18.0, 'precipitacao_media': 1800, 'risco_geada': 'Alto'},
    {'cidade': 'Santa Maria', 'estado': 'RS', 'lat': -29.68, 'lon': -53.80, 'temperatura_media': 20.0, 'precipitacao_media': 1750, 'risco_geada': 'Medio'},
    {'cidade': 'Pelotas', 'estado': 'RS', 'lat': -31.77, 'lon': -52.34, 'temperatura_media': 19.0, 'precipitacao_media': 1600, 'risco_geada': 'Baixo'},
    {'cidade': 'Ijui', 'estado': 'RS', 'lat': -28.38, 'lon': -53.91, 'temperatura_media': 19.5, 'precipitacao_media': 1850, 'risco_geada': 'Medio'},
    {'cidade': 'Chapeco', 'estado': 'SC', 'lat': -27.10, 'lon': -52.61, 'temperatura_media': 20.0, 'precipitacao_media': 1900, 'risco_geada': 'Medio'},
    {'cidade': 'Lages', 'estado': 'SC', 'lat': -27.81, 'lon': -50.32, 'temperatura_media': 17.0, 'precipitacao_media': 1600, 'risco_geada': 'Alto'},
    {'cidade': 'Joacaba', 'estado': 'SC', 'lat': -27.17, 'lon': -51.50, 'temperatura_media': 18.5, 'precipitacao_media': 1700, 'risco_geada': 'Medio'},
    {'cidade': 'Londrina', 'estado': 'PR', 'lat': -23.31, 'lon': -51.16, 'temperatura_media': 23.0, 'precipitacao_media': 1600, 'risco_geada': 'Baixo'},
    {'cidade': 'Cascavel', 'estado': 'PR', 'lat': -24.95, 'lon': -53.45, 'temperatura_media': 22.0, 'precipitacao_media': 1700, 'risco_geada': 'Medio'},
    {'cidade': 'Ponta Grossa', 'estado': 'PR', 'lat': -25.09, 'lon': -50.16, 'temperatura_media': 19.5, 'precipitacao_media': 1550, 'risco_geada': 'Medio'},
    {'cidade': 'Guarapuava', 'estado': 'PR', 'lat': -25.39, 'lon': -51.45, 'temperatura_media': 18.0, 'precipitacao_media': 1650, 'risco_geada': 'Alto'},
    {'cidade': 'Dourados', 'estado': 'MS', 'lat': -22.22, 'lon': -54.80, 'temperatura_media': 24.0, 'precipitacao_media': 1500, 'risco_geada': 'Baixo'},
    {'cidade': 'Campo Grande', 'estado': 'MS', 'lat': -20.44, 'lon': -54.64, 'temperatura_media': 25.0, 'precipitacao_media': 1450, 'risco_geada': 'Baixo'},
    {'cidade': 'Cuiaba', 'estado': 'MT', 'lat': -15.59, 'lon': -56.09, 'temperatura_media': 28.0, 'precipitacao_media': 1400, 'risco_geada': 'Baixo'},
    {'cidade': 'Sinop', 'estado': 'MT', 'lat': -11.86, 'lon': -55.50, 'temperatura_media': 27.0, 'precipitacao_media': 2000, 'risco_geada': 'Baixo'},
    {'cidade': 'Rondonopolis', 'estado': 'MT', 'lat': -16.47, 'lon': -54.63, 'temperatura_media': 26.0, 'precipitacao_media': 1400, 'risco_geada': 'Baixo'},
    {'cidade': 'Sorriso', 'estado': 'MT', 'lat': -12.54, 'lon': -55.71, 'temperatura_media': 26.5, 'precipitacao_media': 1900, 'risco_geada': 'Baixo'},
    {'cidade': 'Rio Verde', 'estado': 'GO', 'lat': -17.79, 'lon': -50.92, 'temperatura_media': 25.0, 'precipitacao_media': 1700, 'risco_geada': 'Baixo'},
    {'cidade': 'Jatai', 'estado': 'GO', 'lat': -17.88, 'lon': -51.71, 'temperatura_media': 24.5, 'precipitacao_media': 1650, 'risco_geada': 'Baixo'},
    {'cidade': 'Barreiras', 'estado': 'BA', 'lat': -12.14, 'lon': -44.99, 'temperatura_media': 26.0, 'precipitacao_media': 1300, 'risco_geada': 'Baixo'},
    {'cidade': 'Luis Eduardo Magalhaes', 'estado': 'BA', 'lat': -12.09, 'lon': -45.80, 'temperatura_media': 25.5, 'precipitacao_media': 1200, 'risco_geada': 'Baixo'}
]

# A logica de "inflar" para 100 foi removida.

df = pd.DataFrame(perfis_base_reais, columns=['cidade', 'estado', 'lat', 'lon', 'temperatura_media', 'precipitacao_media', 'risco_geada'])
df.to_csv('clima_cidades.csv', index=False, encoding='utf-8')

print(f"Arquivo 'clima_cidades.csv' criado com {len(df)} cidades reais (perfis).")