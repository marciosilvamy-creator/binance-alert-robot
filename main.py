import requests
import time

def get_symbols():
    url = "https://api.binance.com/api/v3/ticker/price"
    data = requests.get(url).json()

    symbols = []

    for item in data:
        if item["symbol"].endswith("USDT"):
            symbols.append(item["symbol"])

    return symbols


def get_candles(symbol):

    url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval=1m&limit=60"

    data = requests.get(url).json()

    closes = [float(candle[4]) for candle in data]
    volumes = [float(candle[5]) for candle in data]

    return closes, volumes


def analyze(symbol):

    closes, volumes = get_candles(symbol)

    price_start = closes[0]
    price_end = closes[-1]

    volume_start = volumes[0]
    volume_end = volumes[-1]

    price_change = ((price_end - price_start) / price_start) * 100

    volume_change = ((volume_end - volume_start) / volume_start) * 100

    if price_change > 1 and volume_change > 20:
        return price_change, volume_change

    return None


def scan():

    symbols = get_symbols()

    signals = []

    for symbol in symbols[:80]:

        try:
            result = analyze(symbol)

            if result:
                signals.append((symbol, result[0], result[1]))

        except:
            pass

    signals.sort(key=lambda x: x[1], reverse=True)

    print("\n🚀 POSSÍVEIS OPORTUNIDADES\n")

    for s in signals[:5]:
        print(f"{s[0]} | preço: {round(s[1],2)}% | volume: {round(s[2],2)}%")


while True:

    try:
        scan()
    except Exception as e:
        print("Erro:", e)

    time.sleep(300)
