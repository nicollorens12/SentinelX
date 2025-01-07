from django.shortcuts import render
from django.core.cache import cache  # Importa la cache de Django
from django.core.mail import send_mail  # Para enviar correos
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from pymongo import MongoClient
from bson.json_util import dumps
from bson import json_util
from bson.objectid import ObjectId
import json
import random
from datetime import datetime
import pandas as pd
from api.Hierarchical import HierarchyModel
import smtplib
import os
from dotenv import load_dotenv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

s = smtplib.SMTP('smtp.gmail.com', 587)
# start TLS for security
s.starttls()
# Authentication
load_dotenv()  # Load environment variables from .env file

s.login(os.getenv("EMAIL_SENDER"), os.getenv("EMAIL_SENDER_PSWD"))

hierarchy_model = HierarchyModel(
    model_lvl1='api/LayerModels/model_lvl1_rf.joblib',
    model_lvl2='api/LayerModels/model_lvl2_mlp.joblib',
    model_lvl3='api/LayerModels/model_lvl3_xgb.joblib',
    encoder_lvl2='api/LayerModels/label_encoder_lvl2.joblib',
    encoder_lvl3='api/LayerModels/label_encoder_lvl3.joblib'
)

client = MongoClient('mongodb+srv://Richard:richardADMIN@sentinelx.hwhts.mongodb.net/')

db = client["SentinelX"]

@api_view(['GET'])
def get_history(request):


    documents = list(db.logs_attacks.find({}))
    filtered_data = [
        {   
            "_id": doc.get("_id"),
            "AttackType": doc.get("AttackType"),
            "IP": doc.get("IP"),
            "Port": doc.get("Port"),
            "Date": doc.get("Date")
        }
        for doc in documents
    ]
    json_data = json.loads(json_util.dumps(filtered_data))
    return Response(json_data)

@api_view(['GET'])
def get_history_details(request, document_id):
    document = db.logs_attacks.find_one({"_id": ObjectId(document_id)})
    attack_type = document.get("AttackType")
    filtered_document = {"IP": document.get("IP"), "Port": document.get("Port"), "AttackType": attack_type}

    if attack_type == "DDoS":
        filtered_document.update({
            "Flow Bytes s": document.get("Flow Bytes/s"),
            "Flow Packets s": document.get("Flow Packets/s"),
            "Bwd Packets s": document.get("Bwd Packets/s"),
            "Total Fwd Packets": document.get("Total Fwd Packets"),
            "Total Backward Packets": document.get("Total Backward Packets"),
            "Fwd IAT Std": document.get("Fwd IAT Std"),
            "Bwd IAT Std": document.get("Bwd IAT Std")
        })
    elif attack_type == "XSS":
        filtered_document.update({
            "Fwd PSH Flags": document.get("Fwd PSH Flags"),
            "Subflow Bwd Packets": document.get("Subflow Bwd Packets"),
            "Bwd Packet Length Std": document.get("Bwd Packet Length Std"),
            "Fwd Packet Length Max": document.get("Fwd Packet Length Max"),
            "Fwd Packet Length Std": document.get("Fwd Packet Length Std")
        })
    elif attack_type == "BruteForce":
        filtered_document.update({
            "SYN Flag Count": document.get("SYN Flag Count"),
            "Fwd Packets s": document.get("Fwd Packets/s"),
            "Flow Duration": document.get("Flow Duration"),
            "Idle Min": document.get("Idle Min"),
            "Idle Max": document.get("Idle Max"),
            "Idle Mean": document.get("Idle Mean")
        })
    elif attack_type == "SQLInjection":
        filtered_document.update({
            "Fwd PSH Flags": document.get("Fwd PSH Flags"),
            "Fwd Packet Length Max": document.get("Fwd Packet Length Max"),
            "Fwd Packet Length Std": document.get("Fwd Packet Length Std"),
            "Subflow Fwd Packets": document.get("Subflow Fwd Packets"),
            "Flow Bytes s": document.get("Flow Bytes/s")
        })
    elif attack_type == "PortScan":
        filtered_document.update({
            "Fwd IAT Min": document.get("Fwd IAT Min"),
            "Fwd IAT Max": document.get("Fwd IAT Max"),
            "Fwd IAT Std": document.get("Fwd IAT Std"),
            "Subflow Fwd Packets": document.get("Subflow Fwd Packets"),
            "Flow IAT Min": document.get("Flow IAT Min"),
            "Flow IAT Max": document.get("Flow IAT Max"),
            "Flow IAT Std": document.get("Flow IAT Std"),
            "Fwd Packets s": document.get("Fwd Packets/s")
        })
    return Response(filtered_document)

@api_view(['GET'])
def get_history_more_datails(request, document_id):
    document = db.logs_attacks.find_one({"_id": ObjectId(document_id)})
    json_data = json.loads(json_util.dumps(document))
    return Response(json_data)

# Lista de variables esperadas
expected_variables = [
    "Fwd IAT Std","Bwd Packet Length Max","Idle Mean","Subflow Fwd Packets","Fwd IAT Min","Bwd IAT Max","Idle Min",
    "Idle Std","Bwd IAT Total","Avg Fwd Segment Size","Fwd Packet Length Std","Bwd Packets/s","Flow IAT Min","Idle Max",
    "Bwd IAT Min","Bwd Packet Length Mean","Active Std","Bwd Header Length","Flow Bytes/s","Packet Length Mean","Subflow Bwd Packets",
    "Bwd Packet Length Std","Total Fwd Packets","Fwd PSH Flags","Subflow Bwd Bytes","Fwd Packets/s","Avg Bwd Segment Size",
    "Fwd Packet Length Max","Fwd Header Length","Total Backward Packets","Flow IAT Std","Flow Packets/s","Packet Length Variance",
    "Active Mean","Active Max","Fwd IAT Total","Bwd IAT Std","Active Min","Subflow Fwd Bytes","Fwd IAT Max","URG Flag Count","Flow Duration","Fwd IAT Mean",
    "Fwd Packet Length Mean","Bwd IAT Mean","SYN Flag Count","Flow IAT Mean","Flow IAT Max","Packet Length Std",
]

# Configuraciones del correo (puedes configurarlo en settings.py o como constantes aquí)
EMAIL_FROM = 'nickskate23@gmail.com'  # Cambia esto al correo que usas para enviar
EMAIL_TO = 'nickskate23@gmail.com'  # Cambia esto al correo del destinatario
EMAIL_SUBJECT_TEMPLATE = "ALERTA ATAQUE {attack_type}"  # Plantilla para el asunto del correo
EMAIL_BODY_TEMPLATE = "Has recibido un ataque {attack_type}"  # Plantilla para el cuerpo del correo
CACHE_TIMEOUT = 60  # Tiempo de espera de 60 segundos para evitar múltiples correos

@api_view(['POST'])
def process_traffic(request):
    try:
        input_data = request.data

        # Verificar si faltan variables requeridas
        missing_vars = [var for var in expected_variables if var not in input_data]
        if missing_vars:
            return Response(
                {"error": f"Missing required fields: {', '.join(missing_vars)}."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Crear DataFrame con los datos de entrada
        data = pd.DataFrame([input_data], columns=expected_variables)

        # Realizar la predicción
        predictions = hierarchy_model.predict(data)
        prediction_label = predictions.tolist()[0]  # Obtener la predicción como cadena
        
        if prediction_label != "BENIGN":
            save_attack(input_data, prediction_label)  # Guardar el ataque detectado

            # Verificar si ha pasado suficiente tiempo desde la última alerta de este tipo de ataque
            cache_key = f"attack_alert_{prediction_label}"  # Clave única para la cache por tipo de ataque
            last_alert_time = cache.get(cache_key)
            
            if not last_alert_time:  # Si no hay un registro en la cache, se envía el correo
                send_attack_email(prediction_label)  # Enviar el correo de alerta
                cache.set(cache_key, True, CACHE_TIMEOUT)  # Guardar en cache con tiempo de expiración

        return Response({"predictions": predictions.tolist()}, status=status.HTTP_200_OK)
    
    except Exception as e:
        # Manejo de errores
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

load_dotenv()  # Cargar variables de entorno

def send_attack_email(attack_type):
    """
    Envía un correo electrónico notificando sobre el ataque detectado.
    """
    subject = EMAIL_SUBJECT_TEMPLATE.format(attack_type=attack_type)
    body = EMAIL_BODY_TEMPLATE.format(attack_type=attack_type)
    from_email = os.getenv("EMAIL_SENDER")
    to_email = os.getenv("EMAIL_RECEIVER")

    try:
        # Crear conexión SMTP en cada envío
        with smtplib.SMTP('smtp.gmail.com', 587) as s:
            s.starttls()  # Iniciar TLS
            s.login(from_email, os.getenv("EMAIL_SENDER_PSWD"))  # Iniciar sesión

            # Construir el mensaje
            msg = MIMEMultipart()
            msg['From'] = from_email
            msg['To'] = to_email
            msg['Subject'] = subject
            msg.attach(MIMEText(body, 'plain'))
            
            # Enviar el correo
            s.sendmail(from_email, to_email, msg.as_string())
            print(f"Correo de alerta enviado para el ataque {attack_type}")
    except Exception as e:
        print(f"Error al enviar el correo: {e}")



def generate_ip():
    clase = random.choice(['B', 'C'])
    if clase == 'B':
        first_byte = random.randint(128, 191)
    else:
        first_byte = random.randint(192, 223)

    
    second_byte = random.randint(0, 255)
    third_byte = random.randint(0, 255)
    fourth_byte = random.randint(0, 255)

    ip = f"{first_byte}.{second_byte}.{third_byte}.{fourth_byte}"
    return ip

def save_attack(input_data, attack_type):
    input_data["AttackType"] = attack_type
    input_data["IP"] = generate_ip()
    if attack_type != "PortScan":
        input_data["Port"] = f"{random.randint(1024, 65535)}"
    date = datetime.now().isoformat()
    input_data["Date"] = {"$date": date}

    db.logs_attacks.insert_one(json.loads(json_util.dumps(input_data)))


#Mostrar detalles para:
#DDoS: 
#Flow_Bytes_s,
#Flow_Packets_s, 
#Bwd_Packets_s,
#Total_Fwd_Packets,
#Total_Backward_Packets,
#Fwd_IAT_Std,
#Bwd_IAT_Std
#IP
#Port
#AttackType
#
#XSS:
#Fwd_PSH_Flags,
#Subflow_Bwd_Packets,
#Bwd_Packet_Length_Std,
#Fwd_Packet_Length_Max,
#Fwd_Packet_Length_Std
#IP
#Port
#AttackType
#
#BruteForce:
#SYN_Flag_Count,
#Fwd_Packets_s,
#Flow_Duration,
#Idle_Min,
#Idle_Max,
#Idle_Mean
#IP
#Port
#AttackType
#
#SQLInjection:
#Fwd_PSH_Flags,
#Fwd_Packet_Length_Max,
#Fwd_Packet_Length_Std,
#Subflow_Fwd_Packets,
#Flow_Bytes_s
#IP
#Port
#AttackType
#
#PortScan:
#Fwd_IAT_Min
#Fwd_IAT_Max
#Fwd_IAT_Std
#Subflow_Fwd_Packets
#Flow_IAT_Min
#Flow_IAT_Max
#Flow_IAT_Std
#Fwd_Packets_s
#AttackType