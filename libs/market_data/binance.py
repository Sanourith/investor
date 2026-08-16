from datetime import datetime
from pathlib import Path

import pandas as pd
import requests

binance_url = "https://api.binance.com/"
binance_api = "api/v3/klines"
BASE_URL = f"{binance_url}{binance_api}"
OUTPUT_DIR = Path("data/raw")
FILENAME_TEMPLATE = "BINANCE_{symbol}_1d.csv"
INTERVAL = "1d"  # 1 day

COLUMNS = [
    "open_time",
    "open",
    "high",
    "low",
    "close",
    "volume",
    "close_time",
    "quote_assert_volume",
    "nb_trades",
    "taker_buy_base_volume",
    "taker_buy_quote_volume",
    "ignore",
]


def fetch_klines(symbol: str, interval: str, start_ms: int, end_ms: int) -> list:
    params = {
        "symbol": symbol,
        "interval": interval,
        "startTime": start_ms,
        "endTime": end_ms,
        "limit": 1000,
    }

    response = requests.get(BASE_URL, params=params, timeout=10)
    response.raise_for_status()  # shows exception if fail
    return response.json()


def klines_to_dataframe(klines: list) -> pd.DataFrame:
    df = pd.DataFrame(klines, columns=COLUMNS)

    num_cols = [
        "open",
        "high",
        "low",
        "close",
        "volume",
        "quote_assert_volume",
        "taker_buy_base_volume",
        "taker_buy_quote_volume",
    ]

    df[num_cols] = df[num_cols].astype(float)
    df["open_time"] = pd.to_datetime(df["open_time"], unit="ms", utc=True)
    df["close_time"] = pd.to_datetime(df["close_time"], unit="ms", utc=True)

    # Sellors volume data
    df["taker_sell_base_volume"] = df["volume"] - df["taker_buy_base_volume"]
    df["taker_sell_quote_volume"] = (
        df["quote_assert_volume"] - df["taker_buy_quote_volume"]
    )

    df = df.drop(columns=["ignore"])
    return df


def save_to_csv(dataframe: pd.DataFrame, symbol: str) -> Path:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    filepath = OUTPUT_DIR / FILENAME_TEMPLATE.format(symbol=symbol)

    if filepath.exists():
        existing = pd.read_csv(filepath, parse_dates=["open_time", "close_time"])
        combined = pd.concat([existing, dataframe], ignore_index=True)
        combined = combined.drop_duplicates(subset="open_time", keep="last")
        combined = combined.sort_values("open_time").reset_index(drop=True)
    else:
        combined = dataframe

    combined.to_csv(filepath, index=False)
    return filepath


def process_symbol(
    symbol: str, start_ms: int, end_ms: int, reference_date: datetime
) -> None:
    print(f"Getting {symbol} data from {reference_date.strftime('%d/%m/%Y')} (UTC)...")

    try:
        klines = fetch_klines(symbol, INTERVAL, start_ms, end_ms)
    except Exception as exc:
        print(f"ERROR [{symbol}] : fetch failed ({exc})")
        return

    if not klines:
        print(f"ERROR [{symbol}] : No data requested #check symbol & hour")
        return

    df = klines_to_dataframe(klines)
    filepath = save_to_csv(df, symbol)
    print(
        f"[{symbol}] row for {reference_date.strftime('%d/%m/%Y')} saved at {filepath}"
    )
