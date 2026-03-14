import requests
import time
import json

BASE_URL = "https://api.binance.com"

known_file = "known_symbols.json"


def load_known():

    try:
        with open(known_file, "r") as f:
            return json.load(f)
    except:
        return []


def save_known(symbols):

    with open(known_file, "w") as f:
        json.dump(symbols, f)


def get_symbols():

    url = f"{BASE_URL}/api/v3/exchangeInfo"

    data = requests.get(url).json()

    symbols = []

    for s in data["symbols"]:

        if s["quoteAsset"] == "USDT" and s["status"] == "TRADING":

            symbols.append(s["symbol"])

    return symbols


def detect_new():

    known = load_known()

    current = get_symbols()

    new_coins = []

    for symbol in current:

        if symbol not in known:

            new_coins.append(symbol)

    if new_coins:

        print("\n🚀 NOVAS MOEDAS DETECTADAS\n")

        for coin in new_coins:

            print(coin)

    save_known(current)


while True:

    try:

        detect_new()

    except Exception as e:

        print("Erro:", e)

    time.sleep(600)
