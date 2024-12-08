from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from pymongo import MongoClient
from bson.json_util import dumps
from bson import json_util
from bson.objectid import ObjectId
import json

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
            "Flow_Bytes_s": document.get("Flow_Bytes_s"),
            "Flow_Packets_s": document.get("Flow_Packets_s"),
            "Bwd_Packets_s": document.get("Bwd_Packets_s"),
            "Total_Fwd_Packets": document.get("Total_Fwd_Packets"),
            "Total_Backward_Packets": document.get("Total_Backward_Packets"),
            "Fwd_IAT_Std": document.get("Fwd_IAT_Std"),
            "Bwd_IAT_Std": document.get("Bwd_IAT_Std")
        })
    elif attack_type == "XSS":
        filtered_document.update({
            "Fwd_PSH_Flags": document.get("Fwd_PSH_Flags"),
            "Subflow_Bwd_Packets": document.get("Subflow_Bwd_Packets"),
            "Bwd_Packet_Length_Std": document.get("Bwd_Packet_Length_Std"),
            "Fwd_Packet_Length_Max": document.get("Fwd_Packet_Length_Max"),
            "Fwd_Packet_Length_Std": document.get("Fwd_Packet_Length_Std")
        })
    elif attack_type == "BruteForce":
        filtered_document.update({
            "SYN_Flag_Count": document.get("SYN_Flag_Count"),
            "Fwd_Packets_s": document.get("Fwd_Packets_s"),
            "Flow_Duration": document.get("Flow_Duration"),
            "Idle_Min": document.get("Idle_Min"),
            "Idle_Max": document.get("Idle_Max"),
            "Idle_Mean": document.get("Idle_Mean")
        })
    elif attack_type == "SQLInjection":
        filtered_document.update({
            "Fwd_PSH_Flags": document.get("Fwd_PSH_Flags"),
            "Fwd_Packet_Length_Max": document.get("Fwd_Packet_Length_Max"),
            "Fwd_Packet_Length_Std": document.get("Fwd_Packet_Length_Std"),
            "Subflow_Fwd_Packets": document.get("Subflow_Fwd_Packets"),
            "Flow_Bytes_s": document.get("Flow_Bytes_s")
        })
    elif attack_type == "PortScan":
        filtered_document.update({
            "Fwd_IAT_Min": document.get("Fwd_IAT_Min"),
            "Fwd_IAT_Max": document.get("Fwd_IAT_Max"),
            "Fwd_IAT_Std": document.get("Fwd_IAT_Std"),
            "Subflow_Fwd_Packets": document.get("Subflow_Fwd_Packets"),
            "Flow_IAT_Min": document.get("Flow_IAT_Min"),
            "Flow_IAT_Max": document.get("Flow_IAT_Max"),
            "Flow_IAT_Std": document.get("Flow_IAT_Std"),
            "Fwd_Packets_s": document.get("Fwd_Packets_s")
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

        if not all(var in input_data for var in expected_variables):
            return Response(
                {"error": "Missing one or more required fields."},
                status=status.HTTP_400_BAD_REQUEST
            )

        data = pd.DataFrame([input_data], columns=expected_variables)

        predictions = hierarchy_model.predict(data)
        ##db.logs_attacks.insert_one(json.loads(dataToSave)) saveToLogs
        return Response({"predictions": predictions.tolist()}, status=status.HTTP_200_OK)

    except Exception as e:
        # Manejo de errores
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

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