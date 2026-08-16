import logging
import os
from datetime import datetime

import pandas as pd
import yfinance as yf

from libs.market_data.models import PriceResult

logger = logging.getLogger(__name__)


def get_prices(tickers: dict[str, str]) -> dict[str, PriceResult]:
    symbols = list(tickers.keys())

    try:
        raw = yf.download(
            symbols,
            period="1d",
            group_by="ticker",
            threads=True,
            progress=False,
        )
    except Exception:
        logger.exception("Failed getting data for %d tickers", len(symbols))
        raw = pd.DataFrame()

    now = datetime.now().strftime("%H:%M:%S")
    results: dict[str, PriceResult] = {}

    for ticker, name in tickers.items():
        price = None
        try:
            if len(symbols) == 1:
                # yfinance ne crée pas de MultiIndex quand il n'y a qu'un seul ticker
                close = raw["Close"]
            else:
                close = raw[ticker]["Close"]

            close = close.dropna()
            if not close.empty:
                price = round(float(close.iloc[-1]), 2)
        except (KeyError, IndexError):
            logger.warning("No data for ticker %s (%s)", ticker, name)

        if price is None:
            logger.warning("File not found: %s (%s), fallback .info", ticker, name)
            price = _fallback_single_price(ticker)

        results[ticker] = {
            "Price": price,
            "Time": now,
        }
    return results


def _fallback_single_price(ticker: str) -> float | None:
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period="1d")
        if not hist.empty:
            return round(float(hist["Close"].iloc[-1]), 2)
    except Exception:
        logger.exception("Failed individual callback for %s", ticker)
    return None


def data_raw_csv(df: pd.DataFrame) -> None:
    date_h = datetime.now().strftime("%y%m%d")
    output_dir = "data/raw"
    os.makedirs(output_dir, exist_ok=True)
    filepath = os.path.join(output_dir, f"stock_values_{date_h}.csv")
    df.to_csv(filepath, index=True)
    logger.info("Data saved at: %s", filepath)
