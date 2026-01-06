import datetime
import pickle
from unittest.mock import patch

import pytz
from django.core.cache import cache
from django.urls import reverse
from freezegun import freeze_time
from rest_framework import status
from rest_framework.test import APITestCase

from config.settings import TIME_ZONE
from habits.models import Habits, HabitsForToday
from habits.tasks import (
    get_habits_for_today,
    get_tasks_in_the_next_hour,
    get_tasks_from_cache_and_send_message,
    CACHE_KEY,
)
from users.models import User


class HabitCRUDTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email="test@test.com")
        self.habit = Habits.objects.create(
            place="Бассейн",
            time=datetime.time(20, 30),
            action="Плавать",
            periodicity=1,
            duration=datetime.timedelta(minutes=2),
            is_pleasure=True,
            is_public=True,
            owner=self.user,
        )
        self.client.force_authenticate(user=self.user)

    def test_habit_create(self):
        """Тест создания привычки"""

        url = reverse(viewname="habits:habit-list")
        data = {
            "place": "Парк",
            "time": datetime.time(20, 30),
            "action": "Гулять",
            "periodicity": 1,
            "reward": "Печенье",
            "duration": datetime.timedelta(minutes=2),
            "is_public": True,
            "owner": self.user.pk,
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habits.objects.all().count(), 2)

    def test_habit_edit(self):
        """Тест изменения привычки"""
        url = reverse(viewname="habits:habit-detail", args=(self.habit.pk,))
        data = {
            "duration": datetime.timedelta(minutes=1),
        }
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Habits.objects.get(place="Бассейн").duration, datetime.timedelta(seconds=60))

    def test_changes_another_user(self):
        """Тест изменения привычки другим пользователем."""
        self.user_2 = User.objects.create(email="test2@test.com")
        self.client.force_authenticate(user=self.user_2)
        url = reverse(viewname="habits:habit-detail", kwargs={"pk": self.habit.pk})
        data = {
            "duration": datetime.timedelta(minutes=1),
        }
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Habits.objects.get(place="Бассейн").duration, datetime.timedelta(seconds=120))

    def test_habit_delete(self):
        """Тест удаления привычки"""
        url = reverse(viewname="habits:habit-detail", args=(self.habit.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Habits.objects.all().count(), 0)

    def test_is_pleasure_and_reward(self):
        """Тест одновременного указания вознаграждения и приятной привычки."""
        url = reverse(viewname="habits:habit-list")
        data = {
            "place": "Парк",
            "time": datetime.time(20, 30),
            "action": "Гулять",
            "periodicity": 1,
            "reward": "Печенье",
            "is_pleasure": True,
            "duration": datetime.timedelta(minutes=2),
            "is_public": True,
            "owner": self.user.pk,
        }
        response = self.client.post(url, data, format="json")
        validation_error_text = response.json().get("non_field_errors")[0]
        expected_text = "У приятной привычки не может быть вознаграждения или связанной привычки!"

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(validation_error_text, expected_text)

    def test_is_pleasure_and_related_habit(self):
        """Тест одновременного указания приятной привычки и связанной привычки."""
        url = reverse(viewname="habits:habit-list")
        data = {
            "place": "Парк",
            "time": datetime.time(20, 30),
            "action": "Гулять",
            "periodicity": 1,
            "related_habit": self.habit.pk,
            "is_pleasure": True,
            "duration": datetime.timedelta(minutes=2),
            "is_public": True,
            "owner": self.user.pk,
        }
        response = self.client.post(url, data, format="json")
        validation_error_text = response.json().get("non_field_errors")[0]
        expected_text = "У приятной привычки не может быть вознаграждения или связанной привычки!"

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(validation_error_text, expected_text)

    def test_periodicity(self):
        """Тест создания привычки с периодом больше 7."""
        url = reverse(viewname="habits:habit-list")
        data = {
            "place": "Парк",
            "time": datetime.time(20, 30),
            "action": "Гулять",
            "periodicity": 8,
            "reward": "Печенье",
            "duration": datetime.timedelta(minutes=2),
            "is_public": True,
            "owner": self.user.pk,
        }
        response = self.client.post(url, data, format="json")
        validation_error_text = response.json().get("non_field_errors")[0]
        expected_text = "Нельзя выполнять привычку реже, чем 1 раз в 7 дней!"

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(validation_error_text, expected_text)

    def test_not_related_habit_and_not_reward(self):
        """Тест создания привычки без вознаграждения или связанной привычки."""
        url = reverse(viewname="habits:habit-list")
        data = {
            "place": "Парк",
            "time": datetime.time(20, 30),
            "action": "Гулять",
            "periodicity": 7,
            "duration": datetime.timedelta(minutes=2),
            "is_public": True,
            "owner": self.user.pk,
        }
        response = self.client.post(url, data, format="json")
        validation_error_text = response.json().get("non_field_errors")[0]
        expected_text = "Необходимо указать вознаграждение ИЛИ связанную привычку"

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(validation_error_text, expected_text)

    def test_related_habit_and_reward(self):
        """Тест одновременного указания вознаграждения и связанной привычки."""
        url = reverse(viewname="habits:habit-list")
        data = {
            "place": "Парк",
            "time": datetime.time(20, 30),
            "action": "Гулять",
            "periodicity": 1,
            "reward": "Печенье",
            "related_habit": self.habit.pk,
            "duration": datetime.timedelta(minutes=2),
            "is_public": True,
            "owner": self.user.pk,
        }
        response = self.client.post(url, data, format="json")
        validation_error_text = response.json().get("non_field_errors")[0]
        expected_text = "Можно указать только вознаграждение ИЛИ связанную привычку"

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(validation_error_text, expected_text)

    def test_duration(self):
        """Тест указания времени выполнения привычки."""
        url = reverse(viewname="habits:habit-list")
        data = {
            "place": "Парк",
            "time": datetime.time(20, 30),
            "action": "Гулять",
            "periodicity": 1,
            "reward": "Печенье",
            "related_habit": self.habit.pk,
            "duration": datetime.timedelta(minutes=6),
            "is_public": True,
            "owner": self.user.pk,
        }
        response = self.client.post(url, data, format="json")
        validation_error_text = response.json().get("non_field_errors")[0]
        expected_text = "Время на выполнение не должно быть более 120 секунд!"

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(validation_error_text, expected_text)


class HabitPublicTestCase(APITestCase):
    def setUp(self):
        self.user_1 = User.objects.create(email="test@test.com")
        self.user_2 = User.objects.create(email="test2@test.com")
        self.habit_1 = Habits.objects.create(
            place="Бассейн",
            time=datetime.time(20, 30),
            action="Плавать",
            periodicity=1,
            duration=datetime.timedelta(minutes=2),
            is_pleasure=True,
            is_public=True,
            owner=self.user_1,
        )
        self.habit_2 = Habits.objects.create(
            place="Бассейн",
            time=datetime.time(20, 30),
            action="Плавать",
            periodicity=1,
            duration=datetime.timedelta(minutes=2),
            is_pleasure=True,
            is_public=False,
            owner=self.user_1,
        )

    def test_get_list_public_habits(self):
        self.client.force_authenticate(user=self.user_2)
        url = reverse("habits:public_habits")
        response = self.client.get(url)
        count = response.json().get("count")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(count, 1)


class TaskLogicTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email="test@test.com")
        self.habit = Habits.objects.create(
            place="Бассейн",
            time=datetime.time(20, 30),
            action="Плавать",
            periodicity=1,
            duration=datetime.timedelta(minutes=2),
            next_due_date=datetime.date(2025, 7, 5),
            is_pleasure=True,
            is_public=True,
            owner=self.user,
        )
        self.habit2 = Habits.objects.create(
            place="Парк",
            time=datetime.time(20, 30),
            action="Гулять",
            periodicity=1,
            duration=datetime.timedelta(minutes=2),
            next_due_date=datetime.date(2025, 7, 5),
            is_pleasure=True,
            is_public=True,
            owner=self.user,
        )

        self.habit3 = Habits.objects.create(
            place="Библиотека",
            time=datetime.time(20, 30),
            action="Читать",
            periodicity=1,
            duration=datetime.timedelta(minutes=2),
            next_due_date=datetime.date(2025, 7, 8),
            is_pleasure=True,
            is_public=True,
            owner=self.user,
        )

    def test_get_habits_for_today(self):
        """Тестирование формирования списка привычек на сегодняшний день."""
        date = datetime.date(2025, 7, 5)
        with freeze_time(date):
            get_habits_for_today()
        result = HabitsForToday.objects.all().count()
        self.assertEqual(result, 2)

    def test_get_tasks_in_the_next_hour(self):
        """Тестирование получения задач в ближайший час и добавления их в кэш."""
        cache.clear()
        tz = pytz.timezone(TIME_ZONE)
        date = datetime.datetime(year=2025, month=7, day=5, hour=20, minute=15)
        date_tz = tz.localize(date)

        with freeze_time(time_to_freeze=date_tz):
            self.habit_td_1 = HabitsForToday.objects.create(
                habit=self.habit,
                time=datetime.time(18, 30),
            )
            self.habit_td_2 = HabitsForToday.objects.create(
                habit=self.habit2,
                time=datetime.time(20, 00),
            )
            self.habit_td_3 = HabitsForToday.objects.create(
                habit=self.habit3,
                time=datetime.time(20, 59),
            )
            get_tasks_in_the_next_hour()
        result = pickle.loads(cache.get(CACHE_KEY))
        self.assertEqual(len(result), 2)

    def test_get_tasks_from_cache_and_send_message(self):
        """Тестирование проверки задачи в кэше и отправления уведомления в тг."""
        cache.clear()
        tz = pytz.timezone(TIME_ZONE)
        date = datetime.datetime(year=2025, month=7, day=5, hour=20, minute=15)
        date_tz = tz.localize(date)

        with freeze_time(time_to_freeze=date_tz):
            fake_cache_data = {
                1: {
                    "time": datetime.time(20, 20),
                    "action": self.habit.action,
                    "place": self.habit.place,
                    "chat_id": 12345678,
                    "is_sent": False,
                },
                2: {
                    "time": datetime.time(20, 15),
                    "action": self.habit2.action,
                    "place": self.habit2.place,
                    "chat_id": 12345678,
                    "is_sent": False,
                },
            }
            cache.set(CACHE_KEY, pickle.dumps(fake_cache_data))
            with patch("habits.services.send_telegram_message"):
                get_tasks_from_cache_and_send_message()
        result = pickle.loads(cache.get(CACHE_KEY))
        self.assertEqual(result[2]["is_sent"], True)
        self.assertEqual(result[1]["is_sent"], False)
