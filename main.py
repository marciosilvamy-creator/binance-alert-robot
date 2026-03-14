import requests
import time

BASE_URL = "https://api.binance.com"

positions = {}

STOP_LOSS = -2
TAKE_PROFIT = 3


def get_symbols():

    url = f"{BASE_URL}/api/v3/exchangeInfo"
    data = requests.get(url).json()

    symbols = []

    for s in data["symbols"]:
        if s["quoteAsset"] == "USDT" and s["status"] == "TRADING":
            symbols.append(s["symbol"])

    return symbols


def get_candles(symbol, limit=30):

    url = f"{BASE_URL}/api/v3/klines?symbol={symbol}&interval=1m&limit={limit}"

    data = requests.get(url).json()

    closes = [float(c[4]) for c in data]
    volumes = [float(c[5]) for c in data]

    return closes, volumes


def analyze(symbol):

    closes, volumes = get_candles(symbol)

    price_change = ((closes[-1] - closes[0]) / closes[0]) * 100

    avg_volume = sum(volumes) / len(volumes)

    volume_spike = (volumes[-1] / avg_volume) * 100

    score = price_change + (volume_spike / 10)

    return score


def scan_market():

    symbols = get_symbols()

    results = []

    print("\n🔎 Escaneando mercado...\n")

    for symbol in symbols:

        try:

            score = analyze(symbol)

            results.append((symbol, score))

        except:
            pass

    results.sort(key=lambda x: x[1], reverse=True)

    top = [coin[0] for coin in results[:3]]

    print("\n🚀 TOP 3 MOEDAS\n")

    for coin in top:
        print(coin)

    return top


def monitor(symbols):

    global positions

    print("\n📊 Monitorando...\n")

    for symbol in symbols:

        try:

            closes, volumes = get_candles(symbol, 20)

            avg_price = sum(closes) / len(closes)

            current_price = closes[-1]

            avg_volume = sum(volumes) / len(volumes)

            current_volume = volumes[-1]

            # sinal de compra
            if symbol not in positions:

                if current_price > avg_price and current_volume > avg_volume:

                    positions[symbol] = current_price

                    print(f"🟢 COMPRA: {symbol} a {current_price}")

            else:

                entry = positions[symbol]

                change = ((current_price - entry) / entry) * 100

                if change <= STOP_LOSS:

                    print(f"🔴 STOP LOSS: vender {symbol} | {round(change,2)}%")

                    del positions[symbol]

                elif change >= TAKE_PROFIT:

                    print(f"🟢 TAKE PROFIT: vender {symbol} | {round(change,2)}%")

                    del positions[symbol]

        except:
            pass


while True:

    try:

        top_coins = scan_market()

        for i in range(10):

            monitor(top_coins)

            time.sleep(60)

    except Exception as e:

        print("Erro:", e)

    time.sleep(300)
