from APIs import bcapi
from flask import Flask, render_template, request, jsonify
from APIs.webpayplus import transaction
from transbank.webpay.webpay_plus.transaction import Transaction
from transbank.common.options import WebpayOptions
from transbank.common.integration_type import IntegrationType
from transbank.common.integration_commerce_codes import IntegrationCommerceCodes
from transbank.common.integration_api_keys import IntegrationApiKeys
from BD.firebase_config import db


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

@app.route('/iniciar_pago', methods=['POST'])
def iniciar_pago():

    try:
        buy_order = request.form['buy_order']
        session_id = request.form['session_id']
        amount = float(request.form['amount'])
        return_url = request.form['return_url']

        response = transaction.create(buy_order, session_id, amount, return_url)
        token = response['token']
        payment_url = response['url']

        return render_template('payment_form.html', payment_url=payment_url, token=token)
    
    except Exception as e:
        print("Error al crear la transacción:", str(e))
        error_message = 'Ocurrió un error al crear la transacción. Por favor, intenta nuevamente.'
        return render_template('error.html', error_message=error_message)
    

@app.route('/confirmacion', methods=['GET', 'POST'])
def confirmacion():
    print("Llegada a la función confirmacion()")
    print("Método de la solicitud:", request.method)

    if request.method == 'POST':
        token = request.form.get('token_ws')
    else:
        token = request.args.get('token_ws')

    print("Token recibido:", token)

    if token:
        try:
            # Configurar las opciones de Webpay
            webpay_options = WebpayOptions(IntegrationCommerceCodes.WEBPAY_PLUS, IntegrationApiKeys.WEBPAY, IntegrationType.TEST)

            # Crear una instancia de la transacción con las opciones de Webpay
            transaction = Transaction(webpay_options)

            print("Confirmando la transacción...")

            # Confirmar la transacción
            response = transaction.commit(token)

            print("Respuesta de la confirmación:", response)

            if response['response_code'] == 0:
                # La transacción fue confirmada exitosamente
                print("La transacción fue confirmada exitosamente")
                return render_template('confirmacion.html', response=response)
            else:
                # La transacción no fue confirmada
                print("La transacción no fue confirmada")
                error_message = 'La transacción no pudo ser confirmada. Por favor, intenta nuevamente.'
                return render_template('error.html', error_message=error_message)
        except Exception as e:
            print("Error al confirmar la transacción:")
            print(str(e))
            import traceback
            traceback.print_exc()
            error_message = 'Ocurrió un error al procesar la transacción. Por favor, intenta nuevamente.'
            return render_template('error.html', error_message=error_message)
    else:
        # El token no fue recibido
        print("Token no proporcionado o inválido")
        error_message = 'Token no proporcionado o inválido.'
        return render_template('error.html', error_message=error_message)


@app.route('/retorno', methods=['GET', 'POST'])
def retorno():
    if request.method == 'POST':
        token_ws = request.form.get('token_ws')
    else:
        token_ws = request.args.get('token_ws')

    return confirmacion(token_ws)



if __name__ == '__main__':
    app.run(debug=True)
