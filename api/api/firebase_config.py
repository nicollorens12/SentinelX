import firebase_admin
from firebase_admin import credentials, messaging

# Inicializar Firebase
cred = credentials.Certificate("api/keys/sentinelx-52277-firebase-adminsdk-drxa1-561cb60549.json")
firebase_admin.initialize_app(cred)
