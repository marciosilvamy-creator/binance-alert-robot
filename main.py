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

    current_price = closes[-1]
    average_price = sum(closes) / len(closes)

    price_change = ((closes[-1] - closes[0]) / closes[0]) * 100

    avg_volume = sum(volumes) / len(volumes)
    last_volume = volumes[-1]

    volume_spike = (last_volume / avg_volume) * 100

    if current_price > average_price and price_change > 1 and volume_spike > 150:
        return price_change, volume_spike

    return None


def scan_market():

    symbols = get_symbols()

    results = []

    print(f"\n🔎 Analisando {len(symbols)} moedas...\n")

    for symbol in symbols:

        try:

            result = analyze(symbol)

            if result:
                results.append((symbol, result[0], result[1]))

        except:
            pass

    results.sort(key=lambda x: x[1], reverse=True)

    print("\n🚀 POSSÍVEIS BREAKOUTS\n")

    for coin in results[:10]:

        print(f"{coin[0]} | subida: {round(coin[1],2)}% | volume: {round(coin[2],2)}%")


while True:

    try:
        scan_market()

    except Exception as e:
        print("Erro:", e)

    time.sleep(300)
