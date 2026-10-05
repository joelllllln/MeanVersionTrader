import time
from datetime import datetime, timedelta, timezone


from functions import get_data, pct_calc, volitlity_calc, buy_order, sell_order, get_entry_time

COINS = ["BTC/USD", "ETH/USD", "SOL/USD", "XRP/USD", "ADA/USD"]
THRESHOLDS = {"BTC/USD": -7, "ETH/USD": -8, "SOL/USD": -10, "XRP/USD": -6, "ADA/USD": -8}

while True:
    for coin in COINS:
        df = get_data(coin)
        pct_change = pct_calc(df)
        vol_expansion = volitlity_calc(df)
        entry_time = get_entry_time(coin)

        if entry_time is None:   # no trade open, so a buy is allowed
            if pct_change <= THRESHOLDS[coin] and vol_expansion <= -0.07:
                    buy_order(coin)
                    print(f"Buy order Submitted for:{coin}")
        else:                    # trade open, so no new buy (cooldown)
            if datetime.now(timezone.utc) - entry_time > timedelta(hours=24):
                        sell_order(coin)
                        print(f"Sell order Submitted for:{coin}")

    time.sleep(1800)