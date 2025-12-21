from rest_framework import viewsets, generics
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
        serializer.save(owner=self.request.user)

    def get_permissions(self):

        if self.action in ["update", "partial_update"]:
            self.permission_classes = [IsAuthenticated, IsOwner]

        elif self.action == "destroy":
            self.permission_classes = [IsAuthenticated, IsOwner]

        elif self.action == "retrieve":
            self.permission_classes = [IsAuthenticated, IsOwner]

        return [permission() for permission in self.permission_classes]

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.action == "list":
            return queryset.filter(owner=self.request.user)
        return queryset


class HabitListApiVew(generics.ListAPIView):
    serializer_class = HabitSerializer
    queryset = Habits.objects.all()
    pagination_class = HabitPaginator

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(is_public=True).exclude(owner=self.request.user)
