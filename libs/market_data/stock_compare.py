import logging
import os
import re
from datetime import datetime, timedelta
from pathlib import Path

import pandas as pd

logger = logging.getLogger(__name__)
RAW_FILENAME_RE = re.compile(r"stock_values_(\d{2})(\d{2})_(\d{2})\.csv$")


def _parse_raw_filename(filepath: Path, reference_year: int) -> datetime | None:
    match = RAW_FILENAME_RE.search(filepath.name)
    if not match:
        return None

    day, month, hour = (int(x) for x in match.groups())
    try:
        candidate = datetime(reference_year, month, day, hour)
    except ValueError:
        logger.warning("Invalid filename, check dates : %s", filepath.name)
        return None

    if candidate > datetime.now() + timedelta(days=1):
        candidate = candidate.replace(year=reference_year - 1)

    return candidate


def _latest_file_per_day(raw_dir: str) -> dict:
    raw_path = Path(raw_dir)
    now = datetime.now()
    per_day: dict = {}

    for f in raw_path.glob("stock_values_*.csv"):
        parsed = _parse_raw_filename(f, reference_year=now.year)
        if parsed is None:
            continue

        day_key = parsed.date()
        if day_key not in per_day or parsed > per_day[day_key][0]:
            per_day[day_key] = (parsed, f)

    return per_day


def find_comparison_files(raw_dir: str = "data/raw") -> dict:
    per_day = _latest_file_per_day(raw_dir)
    if not per_day:
        raise FileNotFoundError(f"No stock_values_*.csv files found in {raw_dir}")

    sorted_days = sorted(per_day.keys(), reverse=True)
    today_day = sorted_days[0]
    today_file = per_day[today_day][1]

    last_file = per_day[sorted_days[1]][1] if len(sorted_days) > 1 else None
    if last_file is None:
        logger.warning("No J-1 values found")

    target_lastweek = today_day - timedelta(days=7)
    lastweek_day = min(sorted_days, key=lambda d: abs((d - target_lastweek).days))
    lastweek_gap = abs((lastweek_day - target_lastweek).days)

    if lastweek_gap > 2:
        logger.warning(
            "File from last week is %d from today, approx result attempted",
            lastweek_gap,
            lastweek_day,
        )

    lastweek_file = per_day[lastweek_day][1]
    logger.info(
        "Fichiers sélectionnés -> today: %s | last: %s | lastweek: %s",
        today_file.name,
        last_file.name if last_file else "N/A",
        lastweek_file.name,
    )

    return {"today": today_file, "last": last_file, "lastweek": lastweek_file}


def _load_prices(filepath: Path | None, value_col_name: str) -> pd.DataFrame:
    if filepath is None:
        return pd.DataFrame(columns=["Ticker", value_col_name])

    df = pd.read_csv(filepath)
    df = df[["Ticker", "Price"]].rename(columns={"Price": value_col_name})
    return df


def _load_portfolio(portfolio_path: str) -> pd.DataFrame:
    path = Path(portfolio_path)
    if not path.exists():
        logger.warning("Portfolio not found (%s) value will be missing...")
        return pd.DataFrame(colums=["Ticker", "PrixAchat"])

    df = pd.read_csv(path)
    expected_cols = {"Ticker", "PrixAchat"}
    if not expected_cols.issubset(df.columns):
        raise ValueError(
            f"portfolio.csv must contain at least 2 cols : {expected_cols}"
        )

    return df[["Tickers", "PrixAchat"]]


def _pct_change(current: pd.Series, reference: pd.Series) -> pd.Series:
    with pd.option_context("mode.use_inf_as_na", True):
        pct = ((current - reference) / reference) * 100
    return pct.round(2)


def format_pct(value: float | None) -> str:
    if value is None or pd.isna(value):
        return ""
    sign = "+" if value >= 0 else ""
    return f"{sign}{value:.2f}%"


def build_analysis(
    raw_dir: str = "data/raw",
    portfolio_path: str = "data/extracted/portfolio.csv",
) -> pd.DataFrame:
    files = find_comparison_files(raw_dir)

    today_df = pd.read_csv(files["today"])[["Ticker", "Name", "Price"]]
    last_df = _load_prices(files["last"], "PriceLast")
    lastweek_df = _load_prices(files["lastweek"], "PriceLastweek")
    portfolio_df = _load_portfolio(portfolio_path)

    merged = today_df.merge(last_df, on="Ticker", how="left")
    merged = merged.merge(lastweek_df, on="Ticker", how="left")
    merged = merged.merge(portfolio_df, on="Ticker", how="left")

    merged["value_from_last"] = _pct_change(merged["Price"], merged["PriceLast"])
    merged["value_from_lastweek"] = _pct_change(
        merged["Price"], merged["PriceLastweek"]
    )
    merged["value_portfolio"] = _pct_change(merged["Price"], merged["PrixAchat"])

    result = pd.DataFrame(
        {
            "Name": merged["Name"],
            "Ticker": merged["Ticker"],
            "value_day": merged["Price"],
            "value_from_last": merged["value_from_last"].apply(format_pct),
            "value_from_lastweek": merged["value_from_lastweek"].apply(format_pct),
            "value_portfolio": merged["value_portfolio"].apply(format_pct),
        }
    )

    return result


def save_analysis(df: pd.DataFrame, output_dir: str = "data/treated") -> str:
    os.makedirs(output_dir, exist_ok=True)
    date_str = datetime.now().strftime("%d%m")
    filepath = os.path.join(output_dir, f"analysis_{date_str}.csv")
    df.to_csv(filepath, index=False)
    logger.info("Analyse sauvegardée : %s", filepath)
    return filepath
