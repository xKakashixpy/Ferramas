import firebase_admin
from firebase_admin import credentials, db


cred = credentials.Certificate('project_credentials.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://integracion-aa12c-default-rtdb.firebaseio.com'  # Asegúrate de usar la URL correcta de tu Realtime Database
})

db = db.reference('/')
