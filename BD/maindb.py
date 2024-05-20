from DataBase import FirebaseDB

path ="project_credentials.json"
url ="https://integracion-aa12c-default-rtdb.firebaseio.com"

fb_db = FirebaseDB(path,url)

data_to_write = {
'id': 100,    
'nombre': 'esmeril angular',
'precio': 25000,
'descripcion': 'emeril con discos intercambiables',
'stock': 20,
'categoria': 'esmeril'
}
fb_db.write_record('/herramientas/esmeril', data_to_write)