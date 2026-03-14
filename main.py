import requests
import time
import statistics
import json

BASE_URL = "https://api.binance.com"

positions = {}

known_file = "known_symbols.json"

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


def get_candles(symbol, limit=60):

    url = f"{BASE_URL}/api/v3/klines?symbol={symbol}&interval=1m&limit={limit}"

    data = requests.get(url).json()

    closes = [float(c[4]) for c in data]

    volumes = [float(c[5]) for c in data]

    return closes, volumes


def scan_market():

    symbols = get_symbols()

    results = []

    print("\n🔎 ESCANEANDO MERCADO\n")

    for symbol in symbols:

        try:

            closes, volumes = get_candles(symbol)

            price_change = ((closes[-1] - closes[0]) / closes[0]) * 100

            volume_ratio = volumes[-1] / (sum(volumes)/len(volumes))

            score = price_change + volume_ratio

            results.append((symbol, score))

        except:
            pass

    results.sort(key=lambda x: x[1], reverse=True)

    top = results[:5]

    print("\n⭐ MOEDAS MAIS FORTES\n")

    for coin in top:

        print(coin[0], "score", round(coin[1],2))

    return [c[0] for c in top]


def detect_explosion(symbol):

    closes, volumes = get_candles(symbol)

    avg_volume = sum(volumes[:-1]) / len(volumes[:-1])

    volume_ratio = volumes[-1] / avg_volume

    if volume_ratio > 3:

        print(f"🚀 POSSÍVEL EXPLOSÃO {symbol} volume {round(volume_ratio,2)}x")


def detect_new():

    try:

        with open(known_file,"r") as f:

            known = json.load(f)

    except:

        known = []

    current = get_symbols()

    new = [s for s in current if s not in known]

    if new:

        print("\n🆕 NOVAS MOEDAS\n")

        for coin in new:

            print(coin)

    with open(known_file,"w") as f:

        json.dump(current,f)


def monitor_positions():

    global positions

    for symbol in list(positions.keys()):

        entry = positions[symbol]

        current_price = get_candles(symbol,1)[0][-1]

        change = ((current_price-entry)/entry)*100

        if change <= STOP_LOSS:

            print(f"🔴 STOP LOSS {symbol} {round(change,2)}%")

            del positions[symbol]

        elif change >= TAKE_PROFIT:

            print(f"🟢 TAKE PROFIT {symbol} {round(change,2)}%")

            del positions[symbol]


while True:

    try:

        detect_new()

        top_coins = scan_market()

        for coin in top_coins:

            detect_explosion(coin)

            if coin not in positions:

                price = get_candles(coin,1)[0][-1]

                positions[coin] = price

                print(f"📈 SIMULAÇÃO DE COMPRA {coin} a {price}")

        monitor_positions()

    except Exception as e:

        print("Erro:",e)

    time.sleep(300)
