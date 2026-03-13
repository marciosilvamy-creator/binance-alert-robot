import requests
import time

symbol = "BTCUSDT"
price_alert = 70000  # preço que você quer receber alerta

def get_price():
    url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
    
    try:
        response = requests.get(url)
        data = response.json()

        if "price" in data:
            return float(data["price"])
        else:
            print("Erro na resposta da API:", data)
            return None

    except Exception as e:
        print("Erro ao conectar com a Binance:", e)
        return None


while True:
    price = get_price()

    if price:
        print(f"Preço atual do {symbol}: {price}")

        if price >= price_alert:
            print("🚨 ALERTA! O preço passou do valor definido!")

    time.sleep(60)
