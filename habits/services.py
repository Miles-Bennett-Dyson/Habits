import datetime


import requests


def setting_next_date(periodicity):
    """ Функция для установки следующей даты выполнения привычки. """
    today = datetime.date.today()
    return today + datetime.timedelta(days=periodicity)


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
