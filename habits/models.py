from django.db import models

NULLABLE = {'null': True, 'blank': True}

class Habits(models.Model):

    owner = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        verbose_name="Автор записи",
        related_name="owner",
    )
    place = models.CharField(
        max_length=255,
        verbose_name="Место",
        help_text="Введите место, в котором необходимо выполнять привычку"
    )
    time = models.TimeField(
        verbose_name="Время",
        help_text="Введите время, когда необходимо выполнять привычку"
    )

    next_due_date = models.DateTimeField(
        verbose_name="Следующая дата выполнения",
    )

    action = models.CharField(
        max_length=255,
        verbose_name="Действие",
        help_text="Введите действие, которое представляет собой привычка."
    )
    is_pleasure = models.BooleanField(
        default=False,
        verbose_name="Признак приятной привычки"
    )
    related_habit = models.ForeignKey( # Связанная привычка
        "self",
        on_delete=models.SET_NULL,
        **NULLABLE,
        related_name="main_habit",
        verbose_name="Связанная привычка",
        help_text= "Укажите связанную привычку"
    )
    periodicity = models.PositiveIntegerField(
        default=1,
        verbose_name="Периодичность",
        help_text = "Укажите периодичность выполнения привычки для напоминания в днях"
    )
    reward = models.CharField(
        max_length=255,
        **NULLABLE,
        verbose_name="Вознаграждение",
        help_text="Укажите чем себя вознаградить после выполнения"
    )
    duration = models.DurationField(
        verbose_name="Длительность выполнения",
        help_text = "Укажите время в секундах, которое предположительно потратите на выполнение привычки."
    )
    is_public = models.BooleanField(
        default=False,
        verbose_name="Признак публичности",
        help_text = "Укажите можно ли опубликовать привычку в общий доступ, чтобы другие пользователи смогли взять её себе в пример."
    )

    def __str__(self):
        return self.action

    class Meta:
        verbose_name = 'Привычка'
        verbose_name_plural = 'Привычки'
        ordering = ('pk',)

class HourlyTasks(models.Model):

    habit = models.ForeignKey(
        Habits,
        on_delete=models.CASCADE,
        verbose_name="Привычка",
        related_name="habit",
    )
    time = models.TimeField(
        verbose_name="Назначенное время выполнения привычки",
    )

    def __str__(self):
        return self.time

    class Meta:
        verbose_name = 'Привычка'
        verbose_name_plural = 'Привычки'
        ordering = ('pk',)
