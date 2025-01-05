import pandas as pd
import requests
import random
import time
from threading import Thread

csv_file_path = "dataset_reducido.csv"
api_url = "http://13.38.227.46:8000/api/process_traffic/"

dataset = pd.read_csv(csv_file_path)

# Dividir el dataset por tipo de ataque
columns_to_send = dataset.columns[:-1]

dataDDoS = dataset[dataset['AttackType'] == 'DDoS']
dataDDoS = dataDDoS[columns_to_send]
dataPortScan = dataset[dataset['AttackType'] == 'PortScan']
dataPortScan = dataPortScan[columns_to_send]
dataBruteForce = dataset[dataset['AttackType'] == 'BruteForce']
dataBruteForce = dataBruteForce[columns_to_send]
dataXSS = dataset[dataset['AttackType'] == 'XSS']
dataXSS = dataXSS[columns_to_send]
dataSQLI = dataset[dataset['AttackType'] == 'SQLInjection']
dataSQLI = dataSQLI[columns_to_send]
dataBenign = dataset[dataset['AttackType'] == 'BENIGN']
dataBenign = dataBenign[columns_to_send]

# Función para enviar una fila al servidor
def send_row(row):
    try:
        response = requests.post(api_url, json=row)
        if response.status_code == 200:
            response_data = response.json()
            prediction = response_data.get("predictions", "No prediction found")
            print(f"Fila enviada: {row}")
            print(f"Predicción recibida: {prediction}")
        else:
            print(f"Error al enviar: {response.status_code} - {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Error de conexión: {e}")

# Generar tráfico benigno continuamente
def send_benign_traffic():
    while True:
        # Determinar cuántos paquetes benignos enviar en este segundo (entre 6 y 9)
        packets_to_send = random.randint(10, 20)
        for _ in range(packets_to_send):
            random_row = dataBenign.sample(1).to_dict(orient="records")[0]
            send_row(random_row)
        time.sleep(1)

# Generar tráfico de ataque de forma intermitente
def send_attack_traffic():
    while True:
        # Esperar entre 7 y 12 segundos antes del próximo ataque
        time.sleep(random.randint(30, 45))
        
        # Seleccionar el tipo de ataque de forma aleatoria
        attack_type = random.choice([ "XSS", "SQLInjection"])
        attack_data = {
            #"DDoS": dataDDoS,
            #"PortScan": dataPortScan,
            #"BruteForce": dataBruteForce,
            "XSS": dataXSS,
            "SQLInjection": dataSQLI
        }[attack_type]
        
        # Determinar la duración del ataque
        if attack_type in ["DDoS", "PortScan"]:
            duration = random.randint(6, 9)  # Duración en segundos
            end_time = time.time() + duration
            while time.time() < end_time:
                random_row = attack_data.sample(1).to_dict(orient="records")[0]
                send_row(random_row)
                time.sleep(0.1)  # Enviar muchos paquetes rápidamente
        else:
            # Para BruteForce, XSS, SQLInjection (envían menos paquetes)
            random_row = attack_data.sample(1).to_dict(orient="records")[0]
            send_row(random_row)

# Iniciar tráfico benigno y tráfico de ataque en hilos separados
if __name__ == "__main__":
    try:
        benign_thread = Thread(target=send_benign_traffic)
        attack_thread = Thread(target=send_attack_traffic)

        benign_thread.start()
        attack_thread.start()

        benign_thread.join()
        attack_thread.join()
    except KeyboardInterrupt:
        print("Ejecución interrumpida por el usuario.")
