import datetime

import pytz
import requests

from config.settings import TIME_ZONE


def setting_next_date(user_time, periodicity):
    """ Функция для установки следующей даты выполнения привычки. """

    today = datetime.date.today()
    combined_datetime = datetime.datetime.combine(today, user_time)
    tz = TIME_ZONE
    current_tz = pytz.timezone(tz)
    localize_datetime = current_tz.localize(combined_datetime)
    return localize_datetime + datetime.timedelta(days=periodicity)


def send_telegram_message(chat_id, message):
    """ Функция, для отправки уведомлений в чат telegram. """
    params = {
        'text': message,
        'chat_id': chat_id,
    }
    url = 'https://api.telegram.org/bot'
    token = '8057904554:AAGnsyt552hxhsN6tRdB0q2PPhmkrqruPrU'

    response = requests.get(f'{url}{token}/sendMessage', params=params)


if __name__ == '__main__':
    send_telegram_message(1225099467, 'По лбу не дало?')
