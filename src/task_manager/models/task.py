from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class TaskStatus(models.TextChoices):
    CREATED = 'created'
    STARTED = 'started'
    COMPLETED = 'completed'
    CANCELED = 'canceled'
    FAILED = 'failed'

class Tasks(models.Model):
    name = models.CharField(
        max_length=64,
        unique=True,
        verbose_name="Наименование"
    )
    description = models.TextField(
        null=True,
        blank=True,
        verbose_name="Описание"
    )
    status = models.CharField(
        max_length=20,
        choices=TaskStatus.choices,
        default=TaskStatus.CREATED,
        verbose_name="Статус"
    )
    priority = models.IntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5)
        ],
        default=3,
        verbose_name="Приоритетность"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания"
    )
    is_reopened = models.BooleanField(
        default=False,
        verbose_name = "Переоткрывалась ли"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата обновления"
    )

    class Meta:
        ordering = ["-priority","-created_at"]
        db_table = "tasks"
        verbose_name = "Задача"
        verbose_name_plural = "Задачи"