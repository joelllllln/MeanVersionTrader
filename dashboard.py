import streamlit as st 
from alpaca.trading.enums import OrderStatus
from alpaca.trading.requests import GetOrdersRequest
from alpaca.trading.enums import QueryOrderStatus
import pandas as pd
import numpy as np
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce
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

accountinfo = trade_client.get_account()
orders = trade_client.get_orders()
open_orders = trade_client.get_orders(filter=GetOrdersRequest(status=QueryOrderStatus.OPEN))

df_orders = pd.DataFrame([o.dict() for o in orders])
df_open = pd.DataFrame([o.dict() for o in open_orders])
df_account = pd.DataFrame([accountinfo.dict()])

st.title("Crypto Mean Reversion Live Paper Trader")

st.metric(label ="portfolio value", value = df_account["portfolio_value"].iloc[0])
st.metric(label ="status", value = df_account["status"].iloc[0])

st.subheader("live Trades")
st.table(df_open)

st.subheader("All Trades")
st.table(df_orders)


