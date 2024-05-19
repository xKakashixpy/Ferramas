import bcchapi

def obtener_tasa_de_cambio():
    try:
        siete = bcchapi.Siete("ba.vidals@duocuc.cl", "Wani-gushi007")
        tipo_de_cambio = siete.cuadro(
            series=["F073.TCO.PRE.Z.D"],
            nombres=["tipo_de_cambio_dolar"],
            desde="2024-01-01",  
            hasta="2024-12-01",
            frecuencia="D",
            observado={"tipo_de_cambio_dolar": "last"}
        )
        tasa = tipo_de_cambio['tipo_de_cambio_dolar'].iloc[-1]
        return tasa
    except Exception as e:
        print("Error al obtener la tasa de cambio:", e)
        return None

def convertir_moneda(monto, moneda, tasa_usd_clp):
    if moneda.lower() == 'usd':
        resultado = monto * tasa_usd_clp
    elif moneda.lower() == 'clp':
        resultado = monto / tasa_usd_clp
    else:
        resultado = 'Moneda no válida'
    return resultado