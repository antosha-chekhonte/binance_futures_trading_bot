import os
from binance.client import Client

api_key = os.environ.get("binance_api")
api_secret = os.environ.get("binance_secret")
client = Client(api_key, api_secret)

symbol = 'ethusdt'
interval = '5m'
SOCKET = f"wss://fstream.binance.com/ws/{symbol}@kline_{interval}"

SYMBOL = 'ETHUSDT'
INTERVAL = Client.KLINE_INTERVAL_5MINUTE
DATA_RANGE = "1h"

orders = {}
takes = {}
stops = {}
symbols = {}
quantity = 100  # in usd
limit = 2  # limit of open positions in the current timeframe


precisions = {"BTCUSDT": (1, 3), "DOGEUSDT": (5,0), "ETHUSDT": (2, 3), "SOLUSDT": (3, 0), "XRPUSDT": (4, 1)}