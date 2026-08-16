from datetime import datetime, timezone

from libs.common.utils.utils import get_j1_range_utc
from libs.market_data.binance import process_symbol

SYMBOLS = ["BTCEUR", "ETHEUR"]


def main():
    start_ms, end_ms = get_j1_range_utc()
    reference_date = datetime.fromtimestamp(start_ms / 1000, tz=timezone.utc)

    for symbol in SYMBOLS:
        process_symbol(symbol, start_ms, end_ms, reference_date)


if __name__ == "__main__":
    main()
