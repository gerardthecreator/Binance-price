import requests
import json
from datetime import datetime
import pytz

def get_binance_p2p_price():
    # URL del API interna de Binance P2P
    url = "https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search"
    
    # Parámetros para buscar USDT en Bolívares (VES)
    payload = {
        "asset": "USDT",
        "fiat": "VES",
        "merchantCheck": False,
        "page": 1,
        "payTypes": [],
        "publisherType": None,
        "rows": 1,             # Tomamos solo el primer anuncio (mejor precio)
        "tradeType": "BUY"      # "BUY" para ver anuncios de venta de terceros
    }

    print("--- Iniciando consulta a Binance P2P ---")

    try:
        # Hacemos la petición con un tiempo de espera de 10 segundos
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if data['success'] and data['data']:
            # Extraer precio y nombre del anunciante
            raw_price = data['data'][0]['adv']['price']
            vendor_name = data['data'][0]['advertiser']['nickName']
            
            # Formatear el precio a 2 decimales
            formatted_price = "{:.2f}".format(float(raw_price))
            
            # Obtener la hora actual en Venezuela
            tz_ve = pytz.timezone('America/Caracas')
            now_ve = datetime.now(tz_ve)
            # Formato: 25/04/2026 05:30 PM
            dt_string = now_ve.strftime("%d/%m/%Y %I:%M %p")

            # Estructura del JSON que leerá el index.html
            result = {
                "price": formatted_price,
                "vendor": vendor_name,
                "datetime": dt_string
            }

            # Guardar el archivo data.json
            with open('data.json', 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=4)
            
            print(f"✅ Datos guardados: {formatted_price} VES por {vendor_name}")
            print(f"🕒 Hora local: {dt_string}")
        else:
            print("⚠️ Binance respondió con éxito pero no se encontraron anuncios.")

    except Exception as e:
        print(f"❌ Error crítico: {e}")
        # Opcional: Podrías crear un data.json con error para avisar en la web
        error_data = {"price": "Error", "vendor": "API", "datetime": "Error de conexión"}
        with open('data.json', 'w') as f:
            json.dump(error_data, f)

if __name__ == "__main__":
    get_binance_p2p_price()
    
