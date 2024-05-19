import firebase_admin
from firebase_admin import credentials, db

# Ruta correcta al archivo de credenciales
cred = credentials.Certificate('project_credentials.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://integracion-aa12c-default-rtdb.firebaseio.com'  # Asegúrate de usar la URL correcta de tu Realtime Database
})

# Referencia a la base de datos
ref = db.reference('/')

# Prueba la conexión escribiendo y leyendo datos
try:
    # Escribir datos de prueba
    ref.set({
        'test': {
            'message': 'probando base3!'
        }
    })
    
    # Leer los datos de prueba
    result = ref.get()
    print("Conexión exitosa. Datos de prueba:", result)
except Exception as e:
    print("Error al conectar con Firebase:", e)
