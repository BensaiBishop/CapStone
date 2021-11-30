import config
import json
import requests
import alpaca_trade_api as tradeapi

API_KEY = config.API_KEY
SECRET_KEY = config.SECRET_KEY
HEADERS = {'APCA-API-KEY-ID': API_KEY, 'APCA-API-SECRET-KEY': SECRET_KEY}
ENDPOINT = 'https://paper-api.alpaca.markets'
ORDERS_URL = '{}/v2/orders'.format(ENDPOINT)
ACCOUNT_URL = '{}/v2/account'.format(ENDPOINT)
WATCHLIST_URL = '{}/v2/watchlists'.format(ENDPOINT)
CLOCK_URL = '{}/v2/clock'.format(ENDPOINT)
HISTORY_URL = '{}/v2/account/portfolio/history'.format(ENDPOINT)

api = tradeapi.REST(API_KEY,SECRET_KEY,ENDPOINT)


# make requests
def get_account():
    req = requests.get(ACCOUNT_URL, headers=HEADERS)
    return json.loads(req.content)


def clock():
    req = requests.get(CLOCK_URL, headers=HEADERS)
    return json.loads(req.content)


# watchlists
def get_watchlists():
    req = requests.get(WATCHLIST_URL, headers=HEADERS)

    return json.loads(req.content)


def watchlist(name, symbol):
    data = {
        'name': name,
        'symbol': symbol
    }

    req = requests.post(WATCHLIST_URL, json=data, headers=HEADERS)

    return json.loads(req.content)


def add_symbol(watchlist_id, symbol):
    data = {
        'symbol': symbol
    }

    req = requests.post(WATCHLIST_URL, json=data, headers=HEADERS)

    return json.loads(req.content)


# FMP Requests (250 per day)
def getROE(stock):
    income_statement = requests.get(
        f"https://financialmodelingprep.com/api/v3/financials/income-statement/{stock}?period=quarter")
    income_statement = income_statement.json()
    return income_statement


def getHistory():
    req = requests.get(HISTORY_URL, headers=HEADERS)

    return json.loads(req.content)
