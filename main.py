import requests
import time
import smtplib
from datetime import datetime
from binance.client import Client

# =========================
# CONFIGURAÇÕES
# =========================

API_KEY = "COLOQUE_SUA_API_AQUI"
API_SECRET = "COLOQUE_SUA_SECRET_AQUI"

EMAIL_USER = "seuemail@gmail.com"
EMAIL_PASS = "senha_email"
EMAIL_TO = "seuemail@gmail.com"

RISK_PERCENT = 0.05
STOP_LOSS = -2
TAKE_PROFIT = 3

BASE_URL = "https://api.binance.com"

client = Client(API_KEY, API_SECRET)

positions = {}
trade_history = []

# =========================
# PEGAR MOEDAS
# =========================

def get_symbols():

    data = requests.get(BASE_URL + "/api/v3/exchangeInfo").json()

    symbols = []

    for s in data["symbols"]:
        if s["quoteAsset"] == "USDT" and s["status"] == "TRADING":
            symbols.append(s["symbol"])

    return symbols


# =========================
# PREÇO ATUAL
# =========================

def get_price(symbol):

    data = requests.get(
        BASE_URL + "/api/v3/ticker/price?symbol=" + symbol
    ).json()

    return float(data["price"])


# =========================
# SALDO
# =========================

def get_balance():

    balance = client.get_asset_balance(asset="USDT")

    return float(balance["free"])


# =========================
# TAMANHO DA OPERAÇÃO
# =========================

def calculate_trade_size():

    balance = get_balance()

    return balance * RISK_PERCENT


# =========================
# COMPRA
# =========================

def buy(symbol):

    amount = calculate_trade_size()

    order = client.order_market_buy(
        symbol=symbol,
        quoteOrderQty=amount
    )

    price = get_price(symbol)

    positions[symbol] = {
        "buy_price": price,
        "amount": amount
    }

    trade_history.append(f"COMPRA {symbol} preço {price}")

    print("COMPRA:", symbol)


# =========================
# VENDA
# =========================

def sell(symbol):

    asset = symbol.replace("USDT","")

    balance = client.get_asset_balance(asset=asset)

    quantity = float(balance["free"])

    order = client.order_market_sell(
        symbol=symbol,
        quantity=quantity
    )

    price = get_price(symbol)

    trade_history.append(f"VENDA {symbol} preço {price}")

    del positions[symbol]

    print("VENDA:", symbol)


# =========================
# VERIFICAR STOP / PROFIT
# =========================

def check_positions():

    for symbol in list(positions.keys()):

        buy_price = positions[symbol]["buy_price"]

        price = get_price(symbol)

        change = ((price - buy_price) / buy_price) * 100

        if change <= STOP_LOSS or change >= TAKE_PROFIT:

            sell(symbol)


# =========================
# SINAL SIMPLES
# =========================

def simple_signal(symbol):

    price = get_price(symbol)

    if price:
        return "BUY"

    return None


# =========================
# RELATÓRIO EMAIL
# =========================

def send_report():

    text = "RELATÓRIO DIÁRIO\n\n"

    text += "\n".join(trade_history)

    server = smtplib.SMTP("smtp.gmail.com",587)

    server.starttls()

    server.login(EMAIL_USER,EMAIL_PASS)

    server.sendmail(
        EMAIL_USER,
        EMAIL_TO,
        text
    )

    server.quit()


# =========================
# LOOP PRINCIPAL
# =========================

symbols = get_symbols()

last_report_day = None

while True:

    for symbol in symbols[:20]:

        signal = simple_signal(symbol)

        if signal == "BUY" and symbol not in positions:

            buy(symbol)

    check_positions()

    today = datetime.now().day

    if last_report_day != today:

        send_report()

        last_report_day = today

    time.sleep(300)
