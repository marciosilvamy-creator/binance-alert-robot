import requests
import time
import statistics
import json

BASE_URL = "https://api.binance.com"

history_file = "trade_history.json"

STOP_LOSS = -2
TAKE_PROFIT = 3

positions = {}


def save_history(data):

    try:
        with open(history_file, "r") as f:
            history = json.load(f)
    except:
        history = []

    history.append(data)

    with open(history_file, "w") as f:
        json.dump(history, f, indent=4)


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


def detect_signal(symbol):

    closes, volumes = get_candles(symbol)

    avg_volume = sum(volumes[:-1]) / len(volumes[:-1])

    current_volume = volumes[-1]

    volume_ratio = current_volume / avg_volume

    price_change = ((closes[-1] - closes[0]) / closes[0]) * 100

    volatility = statistics.stdev(closes)

    if volume_ratio > 3 and price_change > 1 and volatility < (sum(closes)/len(closes))*0.01:

        return True

    return False


def scan_market():

    symbols = get_symbols()

    signals = []

    print("\n🔎 Escaneando mercado...\n")

    for symbol in symbols:

        try:

            if detect_signal(symbol):

                signals.append(symbol)

        except:
            pass

    return signals[:3]


def monitor():

    global positions

    for symbol in list(positions.keys()):

        entry = positions[symbol]["entry"]

        current_price = get_candles(symbol, 1)[0][-1]

        change = ((current_price - entry) / entry) * 100

        if change <= STOP_LOSS or change >= TAKE_PROFIT:

            result = {

                "symbol": symbol,
                "entry": entry,
                "exit": current_price,
                "change": round(change, 2)

            }

            save_history(result)

            print(f"📊 Trade finalizado {symbol} {round(change,2)}%")

            del positions[symbol]


while True:

    try:

        signals = scan_market()

        for symbol in signals:

            if symbol not in positions:

                entry_price = get_candles(symbol, 1)[0][-1]

                positions[symbol] = {"entry": entry_price}

                print(f"🚀 Nova operação simulada {symbol} a {entry_price}")

        monitor()

    except Exception as e:

        print("Erro:", e)

    time.sleep(60)
