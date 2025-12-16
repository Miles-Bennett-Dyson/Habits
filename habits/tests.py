import datetime

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from habits.models import Habits
from users.models import User


class HabitCRUDTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email="test@test.com")
        self.habit = Habits.objects.create(
            place='Бассейн',
            time=datetime.time(20, 30),
            action='Плавать',
            is_pleasure=True,
            periodicity=1,
            duration='600',
            is_public=True
        )
        self.client.force_authenticate(user=self.user)

    def test_habit_create(self):
        """ Тест создания привычки """

        url = reverse(viewname='habits:habit-list')
        data = {
            'place': 'Парк',
            'time': datetime.time(20, 30),
            'action': 'Гулять',
            'periodicity': 1,
            'reward': 'Печенье',
            'duration': '120',
            'is_public': True,
            "owner": self.user.pk
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habits.objects.all().count(), 2)
