from django.urls import path

from rest_framework.routers import DefaultRouter

from habits.apps import HabitsConfig
from habits.views import HabitsVewSet

app_name = HabitsConfig.name

router = DefaultRouter()
router.register(r'habit', HabitsVewSet, basename='habit')

urlpatterns = [] + router.urls