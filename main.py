import requests
import time

symbol = "BTCUSDT"
price_alert = 70000  # preço que você quer receber alerta

def get_price():
    url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
    data = requests.get(url).json()
    return float(data["price"])

while True:
    price = get_price()
    print(f"Preço atual do {symbol}: {price}")

    if price >= price_alert:
        print("🚨 ALERTA! O preço passou do valor definido!")

    time.sleep(60)
