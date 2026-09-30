import time
from datetime import datetime, timedelta


from functions import get_data, pct_calc, volitlity_calc, buy_order, sell_order

COINS = ["BTC/USD", "ETH/USD", "SOL/USD", "XRP/USD", "ADA/USD"]
THRESHOLDS = {"BTC/USD": -7, "ETH/USD": -8, "SOL/USD": -10, "XRP/USD": -6, "ADA/USD": -8}

entry_time = {coin: None for coin in COINS}

while True:
    for coin in COINS:
        df = get_data(coin)
        pct_change = pct_calc(df)
        vol_expansion = volitlity_calc(df)

        if entry_time[coin] is None:
            if pct_change <= THRESHOLDS[coin] and vol_expansion <= -0.07:
                    buy_order(coin)
                    entry_time[coin] = datetime.utcnow()
                    print(f"Buy order Submitted for:{coin}")
        else:
            if datetime.utcnow() - entry_time[coin] > timedelta(hours=24):
                        sell_order(coin)
                        entry_time[coin] = None
                        print(f"Sell order Submitted for:{coin}")

    time.sleep(1800)