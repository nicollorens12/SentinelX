from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

import pandas as pd
from api.Hierarchical import HierarchyModel


hierarchy_model = HierarchyModel(
    model_lvl1='api/LayerModels/model_lvl1_rf.joblib',
    model_lvl2='api/LayerModels/model_lvl2_mlp.joblib',
    model_lvl3='api/LayerModels/model_lvl3_xgb.joblib',
    encoder_lvl2='api/LayerModels/label_encoder_lvl2.joblib',
    encoder_lvl3='api/LayerModels/label_encoder_lvl3.joblib'
)

@api_view(['GET'])
def get_history(request):
    return Response({"mensaje": "Recibido"})

@api_view(['GET'])
def get_history_details(request):
    return Response({"mensaje": "Recibido"})

@api_view(['POST'])
def saveTo_history(request):
    data = request.data
    return Response({"mensaje": "Esto es post de método interno", "datos": data}, status=status.HTTP_201_CREATED)

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

        return Response({"predictions": predictions.tolist()}, status=status.HTTP_200_OK)

    except Exception as e:
        # Manejo de errores
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)