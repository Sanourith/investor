from datetime import datetime

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

    except Exception as e:
        return {
            "Price": None,
            "Time": datetime.now().strftime("%H:%M:%S"),
            "Error": str(e),
        }
