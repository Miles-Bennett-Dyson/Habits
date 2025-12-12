import re
from datetime import timedelta

from rest_framework.serializers import ValidationError

from habits.models import Habits


class DurationValidator:
    """ Делает проверку на то, что время выполнения не превышает 120 секунд """

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        duration:timedelta = value.get(self.field)
        td = timedelta(seconds=120)
        if duration > td:
            raise ValidationError('Время на выполнение не должны быть более 120 секунд!')

class HabitFieldsValidator:

    def __call__(self, value):
        related_habit = value.get('related_habit') # связанная привычка
        is_pleasure = value.get('is_pleasure') # приятная привычки
        reward = value.get('reward')
        periodicity = value.get('periodicity', 1)


        if related_habit and not related_habit.is_pleasure:
            raise ValidationError('В связанные привычки могут попадать только привычки с признаком приятной привычки!')

        if is_pleasure and reward or is_pleasure and related_habit:
            raise ValidationError('У приятной привычки не может быть вознаграждения или связанной привычки.!')

        if not 8 > periodicity > 0:
            raise ValidationError('Нельзя выполнять привычку реже, чем 1 раз в 7 дней!')
