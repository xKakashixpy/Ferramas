import bcapi
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Ruta para mostrar el conversor de moneda
@app.route('/tipocambio')
def conversor():
    tasa_usd_clp = bcapi.obtener_tasa_de_cambio()
    return render_template('tipocambio.html', tasa_usd_clp=tasa_usd_clp)

# Ruta para manejar la conversión de moneda
@app.route('/convertir', methods=['POST'])
def convertir():
    try:
        datos = request.get_json()
        monto = float(datos['monto'])
        moneda1 = datos['moneda1']
        moneda2 = datos['moneda2']
        tasa_usd_clp = bcapi.obtener_tasa_de_cambio()
        
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

if __name__ == '__main__':
    app.run(debug=True)
