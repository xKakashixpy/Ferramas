from DataBase import FirebaseDB
from DataBase import add_item, get_items

path ="project_credentials.json"
url ="https://integracion-aa12c-default-rtdb.firebaseio.com/"

fb_db = FirebaseDB(path,url)

data_to_write = {
'nombre': 'esmeril angular',
'precio': 25000,
'descripcion': 'emeril con discos intercambiables',
'stock': 20,
'categoria': 'esmeril'
}
fb_db.write_record('/herramientas/esmeril', data_to_write)



def main():
    # Add a new item
    item = {
        'nombre': 'Sample Item',
        'precio': 100,
        'descripcion': '',
        'stock': 1,
        'categoria': ''
    }
    add_item(item)

    # Get all items
    items = get_items()
    for item in items:
        print(item)

if __name__ == '__main__':
    main()