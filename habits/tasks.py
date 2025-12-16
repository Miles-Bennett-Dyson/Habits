import datetime

from celery import shared_task
from django.core.cache import cache
from django.utils import timezone

from habits.models import Habits, HourlyTasks
from habits.services import send_telegram_message


# @shared_task
def daily_habits():
    """ Функция для формирования списка привычек на сегодняшний день. """
    print('сработала dail')
    HourlyTasks.objects.all().delete()
    today = timezone.localdate()
    habits = Habits.objects.filter(next_due_date=today)
    print('Привычки на день:', habits)

    for habit in habits:
        HourlyTasks.objects.create(habit=habit, time=habit.time)

# @shared_task
def get_tasks_in_the_next_hour():
    """ Функция для отслеживания задач в ближайший час """
    key = "hourly_tasks"
    print('сработала tasks_in_the_next_hour')


    if cache.get(key) is not None:
        cache.delete(key)

    time_now = timezone.localtime()
    add_hour_time = time_now + datetime.timedelta(hours=1)
    habits = HourlyTasks.objects.filter(time__lte=add_hour_time.time())
    print('Привычки в час', habits)
    cache.set(key, habits)

# @shared_task
def get_tasks_from_cache():
    """ Функция ежеминутно проверяет задачи и отправляет уведомления в тг """
    key = "hourly_tasks"
    time_now = timezone.localtime()
    delta_time = time_now + datetime.timedelta(minutes=1)
    habits = cache.get(key)
    habits.filter(time__lte=delta_time)
    if habits is not None:
        for habit in habits:
            chat_id = 1225099467
            message = habit
            send_telegram_message(chat_id, message)
