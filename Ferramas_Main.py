import bcapi
from flask import Flask, render_template, request, jsonify


app = Flask(__name__)


#Ruta para usar el convertidor
@app.route('/tipocambio')
def conversor():
    tasa_usd_clp = bcapi.obtener_tasa_de_cambio()
    return render_template('tipocambio.html', tasa_usd_clp=tasa_usd_clp)

# convertidor de moneda 
@app.route('/convertir', methods=['POST'])

def convertir():
    try:
        datos = request.get_json()
        monto = float(datos['monto'])
        moneda = datos['moneda']
        tasa_usd_clp = bcapi.obtener_tasa_de_cambio()
        if tasa_usd_clp:
            resultado = bcapi.convertir_moneda(monto, moneda, tasa_usd_clp)
            return jsonify({'resultado': resultado})
        else:
            return jsonify({'error': 'No se pudo obtener la tasa de cambio'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500