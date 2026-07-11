import os
from datetime import datetime

import pandas as pd
import yfinance as yf

from libs.market_data.models import PriceResult


def get_price(ticker: str) -> PriceResult:
    try:
        stock = yf.Ticker(ticker)

        info = stock.info
        price = info.get("regularMarketPrice") or info.get("currentPrice")

        if price is None:
            hist = stock.history(period="1d")
            if not hist.empty:
                price = hist["Close"].iloc[-1]

        return {
            "Price": round(price, 2) if price is not None else None,
            "Time": datetime.now().strftime("%H:%M:%S"),
        }

    except Exception:
        return {"Price": None, "Time": datetime.now().strftime("%H:%M:%S")}


def data_raw_csv(df: pd.DataFrame) -> None:
    date_h = datetime.now().strftime("%d%m_%H")
    output_dir = "data/raw"
    os.makedirs(output_dir, exist_ok=True)
    filepath = os.path.join(output_dir, f"stock_values_{date_h}.csv")
    df.to_csv(filepath, index=True)
    print(f"Data saved at {filepath}")
