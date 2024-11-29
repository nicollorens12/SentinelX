from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

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