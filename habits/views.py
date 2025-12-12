from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from habits.models import Habits
from habits.paginators import HabitPaginator
from habits.permissions import IsOwner
from habits.serialaizers import HabitSerializer


class HabitsVewSet(viewsets.ModelViewSet):
    serializer_class = HabitSerializer
    queryset = Habits.objects.all()
    pagination_class = HabitPaginator

    def perform_create(self, serializer):
        habit = serializer.save(owner=self.request.user)

    def get_permissions(self):

        if self.action in ['update', 'partial_update']:
            self.permission_classes = [IsAuthenticated, IsOwner]

        elif self.action == 'destroy':
            self.permission_classes = [IsAuthenticated, IsOwner]

        elif self.action == 'retrieve':
            self.permission_classes = [IsAuthenticated, IsOwner]

        return [permission() for permission in self.permission_classes]
