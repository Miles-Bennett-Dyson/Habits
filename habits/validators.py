import re
from datetime import timedelta

from rest_framework.serializers import ValidationError


class DurationValidator:
    """ Делает проверку на то, что время выполнения не превышает 120 секунд """
    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        duration:timedelta = dict(value).get(self.field)
        td = timedelta(seconds=120)
        if duration > td:
            raise ValidationError('Время на выполнение не должны быть более 120 секунд!')
