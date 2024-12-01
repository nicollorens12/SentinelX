from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from firebase_admin import messaging
from fcm_django.models import FCMDevice
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


def send_notification_to_device(token, title, body):
    """Envía una notificación push a un dispositivo específico."""
    message = messaging.Message(
        notification=messaging.Notification(
            title=title,
            body=body,
        ),
        token=token,
    )
    try:
        response = messaging.send(message)
        print(f"Respuesta de Firebase: {response}")
        return response
    except Exception as e:
        print(f"Error al enviar la notificación: {e}")
        return {"error": str(e)}


@api_view(['POST'])
def process_traffic(request):
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

        # Verificar predicción
        prediction_label = predictions[0]
        if prediction_label != "BENIGN":
            # Token del dispositivo (recibido desde la app móvil y almacenado en el backend)
            device_token = request.data.get("device_token")
            if device_token:
                send_notification_to_device(
                    token=device_token,
                    title="Alerta de Tráfico",
                    body=f"Se detectó tráfico malicioso: {prediction_label}"
                )

        return Response({"predictions": predictions.tolist()}, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['POST'])
def test_notification(request):
    device_token = request.data.get("device_token")
    if device_token:
        send_notification_to_device(
            token=device_token,
            title="Prueba de Notificación",
            body="¡Notificación de prueba enviada correctamente!"
        )
        return Response({"message": "Notification sent successfully"})
    return Response({"error": "Device token is required"}, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['POST'])
def register_token(request):
    token = request.data.get('token')
    if token:
        print(f"Token recibido: {token}")  # Agrega esta línea para verificar el token
        device, created = FCMDevice.objects.update_or_create(
            registration_id=token,
            defaults={'active': True, 'type': 'ios'}
        )
        return Response({'status': 'Token registered'})
    return Response({'error': 'Token is required'}, status=400)
