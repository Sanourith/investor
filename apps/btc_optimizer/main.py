from datetime import datetime, timezone

from libs.common.config import get_cost_basis, get_symbols
from libs.common.utils.utils import get_j1_range_utc
from libs.market_data.binance import process_symbol
from libs.market_data.coin_compare import compare_coins


def main():
    start_ms, end_ms = get_j1_range_utc()
    reference_date = datetime.fromtimestamp(start_ms / 1000, tz=timezone.utc)

    for symbol in get_symbols():
        process_symbol(symbol, start_ms, end_ms, reference_date)
        compare_coins(symbol, reference_date, cost_basis=get_cost_basis(symbol))


if __name__ == "__main__":
    main()
