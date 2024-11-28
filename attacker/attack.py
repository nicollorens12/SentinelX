import pandas as pd
import requests
import random
import time

csv_file_path = "dataset_reducido.csv" 
api_url = "https://tu-api-django.com/endpoint" 

dataset = pd.read_csv(csv_file_path)

# Quitar la columna 'AttackType'
columns_to_send = dataset.columns[:-1] 
dataset = dataset[columns_to_send]

def send_random_row():
    random_row = dataset.sample(1).to_dict(orient="records")[0]
    
    try:
        response = requests.post(api_url, json=random_row)
        if response.status_code == 200:
            print(f"Fila enviada exitosamente: {random_row}")
        else:
            print(f"Error al enviar: {response.status_code} - {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Error de conexión: {e}")

try:
    while True:
        send_random_row()
        time.sleep(1) # Esperar 1 segundo   
except KeyboardInterrupt:
    print("Ejecución interrumpida por el usuario.")
