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

    def test_is_pleasure_and_reward(self):
        """ Тест одновременного указания вознаграждения и приятной привычки. """
        url = reverse(viewname='habits:habit-list')
        data = {
            'place': 'Парк',
            'time': datetime.time(20, 30),
            'action': 'Гулять',
            'periodicity': 1,
            'reward': 'Печенье',
            'is_pleasure': True,
            'duration': '120',
            'is_public': True,
            "owner": self.user.pk
        }
        response = self.client.post(url, data, format='json')
        validation_error_text = response.json().get('non_field_errors')[0]
        expected_text = 'У приятной привычки не может быть вознаграждения или связанной привычки!'

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(validation_error_text, expected_text)

    def test_is_pleasure_and_related_habit(self):
        """ Тест одновременного указания приятной привычки и связанной привычки. """
        url = reverse(viewname='habits:habit-list')
        data = {
            'place': 'Парк',
            'time': datetime.time(20, 30),
            'action': 'Гулять',
            'periodicity': 1,
            'related_habit': self.habit.pk,
            'is_pleasure': True,
            'duration': '120',
            'is_public': True,
            "owner": self.user.pk
        }
        response = self.client.post(url, data, format='json')
        validation_error_text = response.json().get('non_field_errors')[0]
        expected_text = 'У приятной привычки не может быть вознаграждения или связанной привычки!'

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(validation_error_text, expected_text)

    def test_periodicity(self):
        """ Тест создания привычки с периодом больше 7. """
        url = reverse(viewname='habits:habit-list')
        data = {
            'place': 'Парк',
            'time': datetime.time(20, 30),
            'action': 'Гулять',
            'periodicity': 8,
            'reward': 'Печенье',
            'duration': '120',
            'is_public': True,
            "owner": self.user.pk
        }
        response = self.client.post(url, data, format='json')
        validation_error_text = response.json().get('non_field_errors')[0]
        expected_text = 'Нельзя выполнять привычку реже, чем 1 раз в 7 дней!'

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(validation_error_text, expected_text)

    def test_not_related_habit_and_not_reward(self):
        """ Тест создания привычки без вознаграждения или связанной привычки. """
        url = reverse(viewname='habits:habit-list')
        data = {
            'place': 'Парк',
            'time': datetime.time(20, 30),
            'action': 'Гулять',
            'periodicity': 7,
            'duration': '120',
            'is_public': True,
            "owner": self.user.pk
        }
        response = self.client.post(url, data, format='json')
        validation_error_text = response.json().get('non_field_errors')[0]
        expected_text = 'Необходимо указать вознаграждение ИЛИ связанную привычку'

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(validation_error_text, expected_text)

    def test_related_habit_and_reward(self):
        """ Тест одновременного указания вознаграждения и связанной привычки. """
        url = reverse(viewname='habits:habit-list')
        data = {
            'place': 'Парк',
            'time': datetime.time(20, 30),
            'action': 'Гулять',
            'periodicity': 1,
            'reward': 'Печенье',
            'related_habit': self.habit.pk,
            'duration': '120',
            'is_public': True,
            "owner": self.user.pk
        }
        response = self.client.post(url, data, format='json')
        validation_error_text = response.json().get('non_field_errors')[0]
        expected_text = 'Можно указать только вознаграждение ИЛИ связанную привычку'

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(validation_error_text, expected_text)
