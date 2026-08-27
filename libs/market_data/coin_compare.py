import shutil
from datetime import datetime, timedelta
from pathlib import Path

import pandas as pd

from libs.market_data.binance import FILENAME_TEMPLATE as RAW_FILENAME_TEMPLATE
from libs.market_data.binance import OUTPUT_DIR as RAW_DIR
from libs.market_data.binance import fetch_current_price

OUTPUT_DIR = Path("data/processed")
FILENAME = "crypto_analysis.csv"
ARCHIVE_DIR = Path("data/outpassed")


def _load_history(symbol: str) -> pd.DataFrame:
    filepath = RAW_DIR / RAW_FILENAME_TEMPLATE.format(symbol=symbol)
    if not filepath.exists():
        raise FileNotFoundError(f"No history for {symbol} {filepath}")

    df = pd.read_csv(filepath, parse_dates=["open_time", "close_time"])
    return df.sort_values("open_time").reset_index(drop=True)


def _pct_change(current: float, past: float | None) -> float | None:
    if past is None or past == 0:
        return None
    return round((current - past) / past * 100, 2)


def _price_n_days_ago(
    history: pd.DataFrame, reference_date: datetime, days: int
) -> float | None:
    target = reference_date - timedelta(days=days)
    candidates = history[history["open_time"] <= target]
    if candidates.empty:
        return None
    return candidates.iloc[-1]["close"]


def build_symbol_row(
    symbol: str, reference_date: datetime, cost_basis: float | None
) -> dict:
    history = _load_history(symbol)
    current_price = round(fetch_current_price(symbol), 2)

    return {
        "crypto": symbol[:-3],
        "current_price": current_price,
        "past_day": _pct_change(
            current_price, _price_n_days_ago(history, reference_date, 0)
        ),
        "past_week": _pct_change(
            current_price, _price_n_days_ago(history, reference_date, 7)
        ),
        "past_month": _pct_change(
            current_price, _price_n_days_ago(history, reference_date, 30)
        ),
        "actual_value": _pct_change(current_price, cost_basis),
    }


##########
##########


def _archive_existing_file(filepath: Path) -> None:
    if not filepath.exists():
        return

    ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H")
    archive_path = ARCHIVE_DIR / f"crypto_analysis_{timestamp}.csv"
    shutil.copy2(filepath, archive_path)


def write_analysis(rows: list[dict]) -> Path:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    filepath = OUTPUT_DIR / FILENAME

    _archive_existing_file(filepath)

    df = pd.DataFrame(rows)
    df.to_csv(filepath, index=False)
    return filepath
