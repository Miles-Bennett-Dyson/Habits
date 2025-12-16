from django.contrib.auth.models import AbstractUser
from django.db import models

NULLABLE = {'null': True, 'blank': True}

class User(AbstractUser):
    email = models.EmailField(unique=True, verbose_name="Электронная почта")
    phone_number = models.CharField(
        max_length=15,
        verbose_name="Номер телефона",
        **NULLABLE,
    )
    avatar = models.ImageField(
        upload_to="users/avatars/",
        verbose_name="Аватар",
        **NULLABLE,
    )
    city = models.CharField(
        max_length=30,
        verbose_name="Город",
        **NULLABLE,
    )
    username = models.CharField(
        max_length=30,
        verbose_name="Никнейм",
        **NULLABLE,
    )
    tg_chat_id = models.PositiveIntegerField(
        verbose_name="ID чата в телеграмм",
        help_text="Введите ID чата в телеграмм",
        **NULLABLE,
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ['pk']
