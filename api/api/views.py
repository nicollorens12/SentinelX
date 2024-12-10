from django.shortcuts import render
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


@api_view(['POST'])
def process_traffic(request):
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

    try:
        input_data = request.data

        missing_vars = [var for var in expected_variables if var not in input_data]
        if missing_vars:# all(var in input_data for var in expected_variables):
            return Response(
                {"error": f"Missing required fields: {', '.join(missing_vars)}."},
                status=status.HTTP_400_BAD_REQUEST
            )

        data = pd.DataFrame([input_data], columns=expected_variables)

        predictions = hierarchy_model.predict(data)
        if predictions.tolist()[0] != "BENIGN":
            save_attack(input_data, predictions.tolist()[0])

        ##db.logs_attacks.insert_one(json.loads(dataToSave)) ##saveToLogs
        return Response({"predictions": predictions.tolist()}, status=status.HTTP_200_OK)

    except Exception as e:
        # Manejo de errores
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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