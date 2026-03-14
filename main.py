import requests
import time
import statistics

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


def get_candles(symbol, limit=50):

    url = f"{BASE_URL}/api/v3/klines?symbol={symbol}&interval=1m&limit={limit}"

    data = requests.get(url).json()

    closes = [float(c[4]) for c in data]
    volumes = [float(c[5]) for c in data]

    return closes, volumes


def calculate_rsi(closes, period=14):

    gains = []
    losses = []

    for i in range(1, len(closes)):
        diff = closes[i] - closes[i-1]

        if diff >= 0:
            gains.append(diff)
            losses.append(0)
        else:
            gains.append(0)
            losses.append(abs(diff))

    avg_gain = sum(gains[-period:]) / period
    avg_loss = sum(losses[-period:]) / period

    if avg_loss == 0:
        return 100

    rs = avg_gain / avg_loss

    rsi = 100 - (100 / (1 + rs))

    return rsi


def calculate_bollinger(closes):

    sma = sum(closes) / len(closes)

    std = statistics.stdev(closes)

    upper = sma + (std * 2)
    lower = sma - (std * 2)

    return upper, lower


def calculate_macd(closes):

    ema12 = sum(closes[-12:]) / 12
    ema26 = sum(closes[-26:]) / 26

    macd = ema12 - ema26

    return macd


def scan_market():

    symbols = get_symbols()

    scores = []

    print("\n🔎 Escaneando mercado...\n")

    for symbol in symbols:

        try:

            closes, volumes = get_candles(symbol)

            change = ((closes[-1] - closes[0]) / closes[0]) * 100

            volume_spike = volumes[-1] / (sum(volumes)/len(volumes))

            score = change + volume_spike

            scores.append((symbol, score))

        except:
            pass

    scores.sort(key=lambda x: x[1], reverse=True)

    top = [coin[0] for coin in scores[:3]]

    print("\n🚀 TOP 3 MOEDAS\n")

    for coin in top:
        print(coin)

    return top


def monitor(symbols):

    global positions

    for symbol in symbols:

        try:

            closes, volumes = get_candles(symbol)

            current_price = closes[-1]

            avg_price = sum(closes) / len(closes)

            rsi = calculate_rsi(closes)

            upper, lower = calculate_bollinger(closes)

            macd = calculate_macd(closes)

            avg_volume = sum(volumes)/len(volumes)

            current_volume = volumes[-1]

            if symbol not in positions:

                if (
                    current_price > avg_price
                    and 50 < rsi < 70
                    and current_volume > avg_volume
                    and current_price < upper
                    and macd > 0
                ):

                    positions[symbol] = current_price

                    print(f"🟢 COMPRA {symbol} | preço {current_price}")

            else:

                entry = positions[symbol]

                change = ((current_price - entry)/entry) * 100

                if change <= STOP_LOSS:

                    print(f"🔴 STOP LOSS {symbol} {round(change,2)}%")

                    del positions[symbol]

                elif change >= TAKE_PROFIT:

                    print(f"🟢 TAKE PROFIT {symbol} {round(change,2)}%")

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
