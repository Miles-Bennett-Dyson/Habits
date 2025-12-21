import datetime
import os

import requests


def setting_next_date(periodicity):
    """Функция для установки следующей даты выполнения привычки."""
    today = datetime.date.today()
    return today + datetime.timedelta(days=periodicity)


def send_telegram_message(chat_id, message):
    """Функция, для отправки уведомлений в чат telegram."""
    url = os.getenv("TELEGRAM_URL")
    tg_token = os.getenv("TELEGRAM_TOKEN")

    params = {
        "text": message,
        "chat_id": chat_id,
    }

    requests.get(f"{url}{tg_token}/sendMessage", params=params)
