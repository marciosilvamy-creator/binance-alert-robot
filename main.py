import requests
import time

BASE_URL = "https://api.binance.com"

def get_symbols():

    url = f"{BASE_URL}/api/v3/exchangeInfo"

    data = requests.get(url).json()

    symbols = []

    for s in data["symbols"]:

        if s["quoteAsset"] == "USDT" and s["status"] == "TRADING":
            symbols.append(s["symbol"])

    return symbols


def get_candles(symbol):

    url = f"{BASE_URL}/api/v3/klines?symbol={symbol}&interval=1m&limit=60"

    data = requests.get(url).json()

    closes = [float(c[4]) for c in data]
    volumes = [float(c[5]) for c in data]

    return closes, volumes


def analyze(symbol):

    closes, volumes = get_candles(symbol)

    first_price = closes[0]
    last_price = closes[-1]

    price_change = ((last_price - first_price) / first_price) * 100

    avg_volume = sum(volumes) / len(volumes)
    last_volume = volumes[-1]

    volume_spike = (last_volume / avg_volume) * 100

    score = price_change + (volume_spike / 10)

    return score, price_change, volume_spike


def scan_market():

    symbols = get_symbols()

    results = []

    print(f"\n🔎 Analisando {len(symbols)} moedas...\n")

    for symbol in symbols:

        try:

            score, price, volume = analyze(symbol)

            results.append((symbol, score, price, volume))

        except:
            pass

    results.sort(key=lambda x: x[1], reverse=True)

    print("\n🚀 TOP 3 MOEDAS MAIS FORTES\n")

    for coin in results[:3]:

        print(
            f"{coin[0]} | score: {round(coin[1],2)} | preço: {round(coin[2],2)}% | volume: {round(coin[3],2)}%"
        )


while True:

    try:
        scan_market()

    except Exception as e:
        print("Erro:", e)

    time.sleep(300)
