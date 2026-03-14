import requests
import time

symbol = "BTCUSDT"

def get_price():
    url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
    data = requests.get(url).json()
    return float(data["price"])

def get_candles():
    url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval=1m&limit=120"
    data = requests.get(url).json()
    closes = [float(candle[4]) for candle in data]
    return closes

def analyze_market():
    prices = get_candles()

    average_price = sum(prices) / len(prices)
    current_price = get_price()

    print(f"Preço atual: {current_price}")
    print(f"Média das últimas 2h: {average_price}")

    if current_price > average_price:
        print("📈 Tendência de ALTA possível")

    elif current_price < average_price:
        print("📉 Tendência de QUEDA possível")

    else:
        print("➡️ Mercado lateral")


while True:
    try:
        analyze_market()
    except Exception as e:
        print("Erro:", e)

    time.sleep(300)
