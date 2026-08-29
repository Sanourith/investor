from datetime import datetime, timezone

from libs.common.config import get_cost_basis, get_symbols, get_telegram_credentials
from libs.common.utils.utils import get_j1_range_utc
from libs.market_data.binance import process_symbol
from libs.market_data.coin_compare import build_alerts, build_symbol_row, write_analysis
from libs.notifications.telegram import send_telegram_message

ALERT_TRESHOLD_PCT = 7.0


def main():
    start_ms, end_ms = get_j1_range_utc()
    reference_date = datetime.fromtimestamp(start_ms / 1000, tz=timezone.utc)

    rows = []
    for symbol in get_symbols():
        process_symbol(symbol, start_ms, end_ms, reference_date)

        try:
            rows.append(
                build_symbol_row(symbol, reference_date, get_cost_basis(symbol))
            )
        except Exception as exc:
            print(f"ERROR: [{symbol}] : {exc}")

    filepath = write_analysis(rows)
    print(f"Last analysis available in {filepath}")

    alerts = build_alerts(rows, treshold=ALERT_TRESHOLD_PCT)
    if alerts:
        message = f"Crypto ({ALERT_TRESHOLD_PCT}%) :\n" + "\n".join(alerts)
        try:
            token, chat_id = get_telegram_credentials()
            send_telegram_message(token, chat_id, message)
        except Exception as exc:
            print(f"ERROR : Telegram failed ({exc})")


if __name__ == "__main__":
    main()
