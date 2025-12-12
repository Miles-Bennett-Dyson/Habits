from rest_framework import viewsets

from habits.models import Habits
from habits.paginators import HabitPaginator
from habits.serialaizers import HabitSerializer


class HabitsVewSet(viewsets.ModelViewSet):
    serializer_class = HabitSerializer
    queryset = Habits.objects.all()
    pagination_class = HabitPaginator

    def perform_create(self, serializer):
        habit = serializer.save(owner=self.request.user)
