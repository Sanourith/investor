import os
from pathlib import Path

from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parents[3]
ENV_PATH = PROJECT_ROOT / "env" / ".env"

load_dotenv(dotenv_path=ENV_PATH)


def get_symbols() -> list[str]:
    raw = os.getenv("SYMBOLS")
    if not raw:
        raise RuntimeError(f"SYMBOLS not defined into {ENV_PATH}")
    return [s.strip() for s in raw.split(",") if s.strip()]


def get_cost_basis(symbol: str) -> float | None:
    asset = symbol[:-3]  # Get 3 first letter for BTC / ETH etc
    env_key = f"VAL_{asset}"
    value = os.getenv(env_key)

    if value is None or value.strip() == "":
        return None

    try:
        return float(value)
    except ValueError:
        raise RuntimeError(
            f"{env_key}='{value}' invalid in {ENV_PATH} (must be an INT or empty)"
        )


def get_telegram_credentials():
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    if not token or not chat_id:
        raise RuntimeError(
            f"TELEGRAM_BOT_TOKEN et TELEGRAM_CHAT_ID must be defined in {ENV_PATH}"
        )
    return token, chat_id
