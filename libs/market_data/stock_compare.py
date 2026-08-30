import logging
import re
from datetime import date, datetime, timedelta
from pathlib import Path

import pandas as pd

logger = logging.getLogger(__name__)
RAW_DIR = Path("data/raw/stock_values")
FILENAME_PATTERN = re.compile(r"stock_values_(\d{6})\.csv")
INDEX_TICKER = "^FCHI"


def _load_all_stock_files() -> pd.DataFrame:
    frames = []
    for filepath in sorted(RAW_DIR.glob("stock_values_*.csv")):
        match = FILENAME_PATTERN.match(filepath.name)
        if not match:
            continue

        file_date = datetime.strptime(match.group(1), "%y%m%d").date()
        df = pd.read_csv(filepath)
        df["date"] = file_date
        frames.append(df)

    if not frames:
        raise FileNotFoundError(f"No files stock_values found into {RAW_DIR}")

    return pd.concat(frames, ignore_index=True)


def _price_at_or_before(
    ticker_history: pd.DataFrame, target: date, max_gap_days: int = 4
) -> float | None:
    candidates = ticker_history[ticker_history["date"] <= target]
    if candidates.empty:
        return None

    closest = candidates.iloc[-1]
    gap = (target - closest["date"]).days
    if gap > max_gap_days:
        return None

    return closest["Price"]


def _skip_weekend_backwards(d: date) -> date:
    """Recule tant que d tombe un samedi ou un dimanche."""
    while d.weekday() >= 5:  # 5 = samedi, 6 = dimanche
        d -= timedelta(days=1)
    return d


def _last_business_day(d: date) -> date:
    return _skip_weekend_backwards()


def _previous_business_day(d: date) -> date:
    return _skip_weekend_backwards(d - timedelta(days=1))


def _pct_change(current: float, past: float | None) -> float | None:
    if past is None or past == 0:
        return None
    return round((current - past) / past * 100, 2)


def _build_ticker_row(
    ticker: str, name: str, all_data: pd.DataFrame, reference_date: date
) -> dict:
    history = all_data[all_data["Ticker"] == ticker].sort_values("date")
    current_price = _price_at_or_before(history, reference_date)
    if current_price is None:
        raise ValueError(
            f"Pas de donnée pour {ticker} à la date de référence {reference_date}"
        )
    current_price = round(current_price, 2)

    last_target = _previous_business_day(reference_date)
    week_target = reference_date - timedelta(days=7)
    month_target = reference_date - timedelta(days=30)

    return {
        "stock": name,
        "current_price": current_price,
        "past_day": _pct_change(
            current_price, _price_at_or_before(history, last_target)
        ),
        "past_week": _pct_change(
            current_price, _price_at_or_before(history, week_target)
        ),
        "past_month": _pct_change(
            current_price, _price_at_or_before(history, month_target)
        ),
        "actual_value": None,  # TODO change when i can extract my PEA portfolio
    }


def build_analysis() -> pd.DataFrame:
    all_data = _load_all_stock_files()
    reference_date = all_data["date"].max()

    tickers = all_data[all_data["Ticker"] != INDEX_TICKER][
        ["Ticker", "Name"]
    ].drop_duplicates()

    rows = []
    for _, ticker_row in tickers.iterrows():
        try:
            rows.append(
                _build_ticker_row(
                    ticker_row["Ticker"], ticker_row["Name"], all_data, reference_date
                )
            )
        except Exception as exc:
            print(f"ERROR for {ticker_row['Ticker']} : {exc}")
    return pd.DataFrame(rows)


def save_analysis(analysis_df: pd.DataFrame) -> Path:
    output_dir = Path("data/processed")
    output_dir.mkdir(parents=True, exist_ok=True)
    filepath = output_dir / "stock_analysis.csv"

    analysis_df.to_csv(filepath, index=False)
    return filepath
