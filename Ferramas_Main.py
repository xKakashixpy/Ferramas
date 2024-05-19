import bcapi
from flask import Flask, render_template, request, jsonify
from webpayplus import transaction
from transbank.webpay.webpay_plus.transaction import Transaction
from transbank.common.options import WebpayOptions
from transbank.common.integration_type import IntegrationType
from transbank.common.integration_commerce_codes import IntegrationCommerceCodes
from transbank.common.integration_api_keys import IntegrationApiKeys
from firebase_config import db


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add', methods=['POST'])
def add_item():
    data = request.json
    new_ref = db.push(data)
    data['id'] = new_ref.key
    new_ref.update({'id': new_ref.key})
    return jsonify({"success": True}), 200

@app.route('/get', methods=['GET'])
def get_items():
    items = db.get()
    result = []
    if items:
        for key, value in items.items():
            result.append(value)
    return jsonify(result), 200

@app.route('/delete/<item_id>', methods=['DELETE'])
def delete_item(item_id):
    db.child(item_id).delete()
    return jsonify({"success": True}), 200





#----------------Aplicacion tipo de Cambio----
@app.route('/tipocambio')
def conversor():
    tasa_usd_clp = bcapi.obtener_tasa_de_cambio("2024-12-01")  # Ejemplo de fecha
    return render_template('tipocambio.html', tasa_usd_clp=tasa_usd_clp)

@app.route('/convertir', methods=['POST'])
def convertir():
    try:
        datos = request.get_json()
        monto = float(datos['monto'])
        moneda1 = datos['moneda1']
        moneda2 = datos['moneda2']
        fecha = datos['fecha']
        tasa_usd_clp = bcapi.obtener_tasa_de_cambio(fecha)
        
        if tasa_usd_clp:
            if moneda1 == "usd" and moneda2 == "clp":
                resultado = bcapi.convertir_moneda(monto, 'usd', tasa_usd_clp)
            elif moneda1 == "clp" and moneda2 == "usd":
                resultado = bcapi.convertir_moneda(monto, 'clp', tasa_usd_clp)
            else:
                resultado = "Conversión no válida"
            return jsonify({'resultado': resultado})
        else:
            return jsonify({'error': 'No se pudo obtener la tasa de cambio'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    

##WEBPAY------


if __name__ == '__main__':
    app.run(debug=True)
