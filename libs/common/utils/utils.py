from datetime import datetime, timedelta, timezone


def get_j1_range_utc() -> tuple[int, int]:
    now_utc = datetime.now(timezone.utc)
    today_midnight = now_utc.replace(hour=0, minute=0, second=0, microsecond=0)
    yesterday_start = today_midnight - timedelta(days=1)
    yesterday_end = today_midnight - timedelta(milliseconds=1)

    start_ms = int(yesterday_start.timestamp() * 1000)
    end_ms = int(yesterday_end.timestamp() * 1000)
    return start_ms, end_ms
