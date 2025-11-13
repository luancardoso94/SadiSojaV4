# Arquivo: treinar_modelo_tf.py (SEM ACENTO)
import pandas as pd
import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder, OrdinalEncoder
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.utils import to_categorical
import joblib

print(f"Versao do TensorFlow: {tf.__version__}")

try:
    df = pd.read_csv('dados_soja.csv')
except FileNotFoundError:
    print("ERRO: Arquivo 'dados_soja.csv' nao encontrado.")
    print("Por favor, execute o script 'gerar_dados_soja.py' primeiro.")
    exit()

print(f"Dados carregados: {df.shape[0]} amostras.")

X = df.drop('risco_plantio', axis=1)
y = df['risco_plantio']

colunas_numericas = ['temperatura_media', 'precipitacao_media']
colunas_categoricas = ['estado', 'cidade', 'janela_plantio']
coluna_ordinal = ['risco_geada']

risco_categorias = ['Baixo', 'Medio', 'Alto']

transformador_numerico = StandardScaler()
transformador_categorico = OneHotEncoder(handle_unknown='ignore', sparse_output=False)
transformador_ordinal = OrdinalEncoder(categories=[risco_categorias])

preprocessor = ColumnTransformer(
    transformers=[
        ('num', transformador_numerico, colunas_numericas),
        ('cat', transformador_categorico, colunas_categoricas),
        ('ord', transformador_ordinal, coluna_ordinal)
    ],
    remainder='passthrough' 
)

print("Aplicando pre-processamento nos dados de entrada (X)...")
X_processed = preprocessor.fit_transform(X)

label_encoder = LabelEncoder()
y_int = label_encoder.fit_transform(y)
y_categorical = to_categorical(y_int) 

classes_alvo = label_encoder.classes_
print(f"Classes de saida (alvo): {classes_alvo}")

num_classes = len(classes_alvo)
num_features = X_processed.shape[1]

print("Definindo a arquitetura da Rede Neural...")
model = Sequential([
    Dense(64, activation='relu', input_shape=[num_features]),
    Dropout(0.2), 
    Dense(32, activation='relu'),
    Dense(num_classes, activation='softmax')
])

model.compile(
    optimizer='adam',
    loss='categorical_crossentropy', 
    metrics=['accuracy']
)
print(model.summary())

print("\nIniciando o treinamento do modelo...")
X_train, X_test, y_train, y_test = train_test_split(X_processed, y_categorical, test_size=0.2, random_state=42)

history = model.fit(
    X_train, y_train,
    epochs=50, batch_size=16, 
    validation_data=(X_test, y_test), 
    verbose=1
)

print("\nTreinamento concluido!")
loss, accuracy = model.evaluate(X_test, y_test, verbose=0)
print(f"Acuracia no conjunto de teste: {accuracy * 100:.2f}%")

model.save('modelo_soja_tf.h5')
print("Modelo TensorFlow salvo em 'modelo_soja_tf.h5'")

joblib.dump(preprocessor, 'preprocessor.pkl')
print("Pre-processador salvo em 'preprocessor.pkl'")

joblib.dump(label_encoder, 'label_encoder.pkl')
print("LabelEncoder salvo em 'label_encoder.pkl'")