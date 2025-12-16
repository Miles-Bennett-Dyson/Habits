import pickle

from celery import shared_task
from django.core.cache import cache
from django.utils import timezone

from habits.models import Habits, HabitsForToday
from habits.services import send_telegram_message

CACHE_KEY = "hourly_tasks"


@shared_task
def get_habits_for_today():
    """ Функция для формирования списка привычек на сегодняшний день. """

    HabitsForToday.objects.all().delete()
    today = timezone.localdate()
    habits = Habits.objects.filter(next_due_date=today)
    if not habits:
        return

    for habit in habits:
        HabitsForToday.objects.create(habit=habit, time=habit.time)


@shared_task
def get_tasks_in_the_next_hour():
    """ Функция для получения задач в ближайший час и добавления их в кэш. """

    if cache.get(CACHE_KEY) is not None:
        cache.delete(CACHE_KEY)

    time_now = timezone.localtime().hour
    habits = HabitsForToday.objects.filter(time__hour=time_now)

    if not habits:
        return

    habits_dict = {}
    for habit in habits:
        habits_dict[habit.pk] = {
            'time': habit.habit.time,
            'action': habit.habit.action,
            'place': habit.habit.place,
            'chat_id': habit.habit.owner.tg_chat_id,
            'is_sent': False
        }
    cache.set(CACHE_KEY, pickle.dumps(habits_dict), 60 * 60)


@shared_task
def get_tasks_from_cache():
    """ Функция ежеминутно проверяет задачи и отправляет уведомления в тг """
    time_now = timezone.localtime().minute
    hourly_tasks = cache.get(CACHE_KEY)
    if hourly_tasks is None:
        return

    loaded = pickle.loads(hourly_tasks)

    for hourly_task in loaded.values():
        habit_time = hourly_task.get('time')
        tg_chat_id = hourly_task.get('chat_id')

        if not tg_chat_id:
            continue

        if not hourly_task.get('is_sent') and habit_time.minute <= time_now:
            habit_action = hourly_task.get('action')
            habit_place = hourly_task.get('place')
            message = f'В {habit_time}, я буду {habit_action} в {habit_place}'
            send_telegram_message(tg_chat_id, message)
            hourly_task['is_sent'] = True
    cache.set(CACHE_KEY, pickle.dumps(loaded), 60 * 60)
