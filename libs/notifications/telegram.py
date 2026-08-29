import requests

TELEGRAM_API_URL = "https://api.telegram.org/bot{token}/sendMessage"


def send_telegram_message(token: str, chat_id: str, text: str) -> None:
    url = TELEGRAM_API_URL.format(token=token)
    response = requests.post(url, data={"chat_id": chat_id, "text": text}, timeout=10)
    response.raise_for_status()
