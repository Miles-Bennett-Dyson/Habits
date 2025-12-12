from django.urls import path

from rest_framework.routers import DefaultRouter

from habits.apps import HabitsConfig
from habits.views import HabitsVewSet, HabitListApiVew

app_name = HabitsConfig.name

router = DefaultRouter()
router.register(r'habit', HabitsVewSet, basename='habit')

urlpatterns = [
    path('public_habits/', HabitListApiVew.as_view(), name='habits'),
              ] + router.urls