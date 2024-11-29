import pandas as pd

# Cargar el dataset
df = pd.read_csv('dataset.csv')

# Reducir aleatoriamente a 250,000 filas
df_reducido = df.sample(n=320000, random_state=1)

# Guardar el nuevo dataset reducido
df_reducido.to_csv('dataset_reducido.csv', index=False)

print("Dataset reducido guardado como 'dataset_reducido.csv'")