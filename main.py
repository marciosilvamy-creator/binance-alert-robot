import requests
import time

def get_symbols():
    url = "https://api.binance.com/api/v3/ticker/price"
    data = requests.get(url).json()

    symbols = []
    for item in data:
        if "USDT" in item["symbol"]:
            symbols.append(item["symbol"])

    return symbols


def get_candles(symbol):
    url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval=1m&limit=120"
    data = requests.get(url).json()

    closes = [float(candle[4]) for candle in data]

    return closes


def analyze_symbol(symbol):
    prices = get_candles(symbol)

    first = prices[0]
    last = prices[-1]

    change = ((last - first) / first) * 100

    return change


def scan_market():

    symbols = get_symbols()

    results = []

    for symbol in symbols[:50]:  # limita para não sobrecarregar
        try:
            change = analyze_symbol(symbol)
            results.append((symbol, change))
        except:
            pass

    results.sort(key=lambda x: x[1], reverse=True)

    print("\n🚀 TOP 3 MOEDAS COM MAIOR SUBIDA\n")

    for coin in results[:3]:
        print(f"{coin[0]}  |  {round(coin[1],2)} %")


while True:

    try:
        scan_market()
    except Exception as e:
        print("Erro:", e)

    time.sleep(300)
