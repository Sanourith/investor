from datetime import datetime, timezone

from libs.common.utils.utils import get_j1_range_utc
from libs.market_data.binance import fetch_klines, klines_to_dataframe, save_to_csv

SYMBOL = "BTCEUR"
INTERVAL = "1d"  # 1 day


def main():
    start_ms, end_ms = get_j1_range_utc()
    reference_date = datetime.fromtimestamp(start_ms / 1000, tz=timezone.utc)

    print(f"Getting BTC/EUR data from {reference_date.strftime('%d/%m/%Y')} (UTC)...")

    klines = fetch_klines(SYMBOL, INTERVAL, start_ms, end_ms)
    if not klines:
        print("ERROR : No data requested #check symbol & hour")
        return

    df = klines_to_dataframe(klines)
    filepath = save_to_csv(df)
    print(f"Row for {reference_date.strftime('%d/%m/%Y')} saved at {filepath}")


if __name__ == "__main__":
    main()
