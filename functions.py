import time
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest, GetOrdersRequest
from alpaca.trading.enums import OrderSide, TimeInForce, QueryOrderStatus
from alpaca.data.historical import CryptoHistoricalDataClient
from alpaca.data.requests import CryptoBarsRequest
from alpaca.data.timeframe import TimeFrame
from dotenv import load_dotenv
import os

load_dotenv()
PAPER_KEY = os.getenv("PAPER_KEY")
PAPER_SECRET = os.getenv("PAPER_SECRET")

trade_client = TradingClient(PAPER_KEY, PAPER_SECRET, paper=True)
#connection to the platform's trading system. Paper-trading account for paper=True
data_client = CryptoHistoricalDataClient()
#retrieve historical cryptocurrency market data.

def get_data(coin):
    request = CryptoBarsRequest(
    symbol_or_symbols=coin,
    timeframe=TimeFrame.Hour,
    start=datetime.now() - timedelta(hours=12))
    #bar set is a candle stick, contains OHLCV data for a specific time frame
    #OHLCV stands for Open, High, Low, Close, Volume.
    #barset is a python object defined using imports above
    bars = data_client.get_crypto_bars(request)
    df = bars.df.reset_index()
    df = df.sort_values("timestamp")
    return df

def pct_calc(df):
    h12 = df["close"].iloc[0]
    h0 = df["close"].iloc[-1]
    pct_change = (h0 - h12) / h12 * 100
    return pct_change

def volitlity_calc(df):
    df["pct_change"] = df["close"].pct_change() * 100
    last12 = df["pct_change"].iloc[-12:]
    std_vol_first_half = last12.iloc[:6].std()
    std_vol_second_half = last12.iloc[6:].std()
    vol_expansion = (std_vol_second_half - std_vol_first_half) / std_vol_first_half
    return vol_expansion

def buy_order(coin):
    order = trade_client.submit_order(
        MarketOrderRequest(
            symbol = coin, 
            notional=100000,
            side=OrderSide.BUY,
            time_in_force=TimeInForce.IOC
        )
    )
#GTG - good till cancelled, stays open until filled or cancelled, limit order
#IOC - immediate or cancel, fills whatever it can right now, cancels the rest
#DAY - cancels at end of trading day if not filled

def sell_order(coin):
    # sells the exact amount you hold
    trade_client.close_position(coin.replace("/", ""))

def get_entry_time(coin):
    # no open position = no trade active
    try:
        trade_client.get_open_position(coin.replace("/", ""))
    except Exception:
        return None
    # find the last buy the loop made for this coin
    orders = trade_client.get_orders(GetOrdersRequest(
        status=QueryOrderStatus.CLOSED,
        symbols=[coin],
        side=OrderSide.BUY,
        limit=1))
    return orders[0].filled_at
