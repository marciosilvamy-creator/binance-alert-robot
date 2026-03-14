import requests
import time
import statistics

BASE_URL = "https://api.binance.com"


def get_symbols():

    url = f"{BASE_URL}/api/v3/exchangeInfo"
    data = requests.get(url).json()

    symbols = []

    for s in data["symbols"]:

        if s["quoteAsset"] == "USDT" and s["status"] == "TRADING":
            symbols.append(s["symbol"])

    return symbols


def get_candles(symbol, limit=60):

    url = f"{BASE_URL}/api/v3/klines?symbol={symbol}&interval=1m&limit={limit}"

    data = requests.get(url).json()

    closes = [float(c[4]) for c in data]
    volumes = [float(c[5]) for c in data]

    return closes, volumes


def analyze_symbol(symbol):

    closes, volumes = get_candles(symbol)

    avg_volume = sum(volumes[:-1]) / len(volumes[:-1])

    current_volume = volumes[-1]

    volume_ratio = current_volume / avg_volume

    price_change = ((closes[-1] - closes[0]) / closes[0]) * 100

    volatility = statistics.stdev(closes)

    liquidity = sum(volumes)

    score = (volume_ratio * 2) + price_change - (volatility * 10)

    return score, volume_ratio, price_change, liquidity


def super_scan():

    symbols = get_symbols()

    opportunities = []

    print("\n🌎 Escaneando todo o mercado...\n")

    for symbol in symbols:

        try:

            score, volume_ratio, price_change, liquidity = analyze_symbol(symbol)

            if liquidity > 100000:

                opportunities.append(
                    (symbol, score, volume_ratio, price_change)
                )

        except:
            pass

    opportunities.sort(key=lambda x: x[1], reverse=True)

    print("\n🚀 TOP 10 OPORTUNIDADES DO MERCADO\n")

    for coin in opportunities[:10]:

        print(
            f"{coin[0]} | score {round(coin[1],2)} | volume {round(coin[2],2)}x | movimento {round(coin[3],2)}%"
        )


while True:

    try:

        super_scan()

    except Exception as e:

        print("Erro:", e)

    time.sleep(300)
