from datetime import datetime
from pathlib import Path

OUTPUT_DIR = Path("data/processed")
FILENAME_TEMPLATE = "Analysis_{symbol}_{reference_date}.csv"


def compare_coins(
    symbol: str, reference_date: datetime, cost_basis: float | None
) -> None:
    print(f"Hello {symbol} {reference_date} {cost_basis}")
