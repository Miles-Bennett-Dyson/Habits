from celery import shared_task
from django.utils import timezone

from habits.models import Habits, HourlyTasks


@shared_task
def daily_habits():
    """ Функция для формирования списка привычек на сегодняшний день. """

    HourlyTasks.objects.all().delete()
    today = timezone.localdate()
    habits = Habits.objects.filter(next_due_date=today)

    for habit in habits:
        HourlyTasks.objects.create(habit=habit, time=habit.time)
