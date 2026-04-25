import requests
import json
from datetime import datetime
import pytz

def get_binance_p2p_price():
    # URL del API interna de Binance P2P
    url = "https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search"
    
    # Configuración de la consulta para VES (Bolívares)
    payload = {
        "asset": "USDT",
        "fiat": "VES",
        "merchantCheck": False,
        "page": 1,
        "payTypes": [],
        "publisherType": None,
        "rows": 1,        # Solo necesitamos el mejor precio
        "tradeType": "BUY" # "BUY" en el API muestra los anuncios de venta (lo que tú pagarías)
    }

    try:
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status() # Lanza error si la petición falla
        data = response.json()
        
        if data['success'] and data['data']:
            # Extraer información relevante
            first_ad = data['data'][0]
            price = first_ad['adv']['price']
            vendor = first_ad['advertiser']['nickName']
            
            # Obtener hora de Venezuela
            tz_ve = pytz.timezone('America/Caracas')
            now_ve = datetime.now(tz_ve)
            dt_string = now_ve.strftime("%d/%m/%Y %I:%M:%S %p")

            # Crear el diccionario de datos
            result = {
                "price": price,
                "vendor": vendor,
                "datetime": dt_string
            }

            # Guardar en data.json
            with open('data.json', 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=4)
            
            print(f"✅ Éxito: {price} VES - {dt_string}")
        else:
            print("❌ No se encontraron anuncios o respuesta fallida.")

    except Exception as e:
        print(f"❌ Error durante la ejecución: {e}")

if __name__ == "__main__":
    get_binance_p2p_price()
  
