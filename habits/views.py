from rest_framework import viewsets

from habits.models import Habits
from habits.serialaizers import HabitSerializer


class HabitsVewSet(viewsets.ModelViewSet):
    serializer_class = HabitSerializer
    queryset = Habits.objects.all()