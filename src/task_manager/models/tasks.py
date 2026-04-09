from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from config.models import BaseModel
from django.db.models.signals import post_save
from django.dispatch import receiver

class TaskStatus(models.TextChoices):
    CREATED = 'created'
    STARTED = 'started'
    COMPLETED = 'completed'
    CANCELED = 'canceled'
    FAILED = 'failed'

class Tasks(BaseModel):
    objects = None
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
    is_reopened = models.BooleanField(
        default=False,
        verbose_name = "Переоткрывалась ли"
    )
    project = models.ForeignKey(
        to="Projects",
        related_name="tasks",
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    assignee = models.ForeignKey(
        to="account.User",
        related_name="tasks",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    class Meta:
        ordering = ["-priority","-created_at"]
        db_table = "tasks"
        verbose_name = "Задача"
        verbose_name_plural = "Задачи"


    def __str__(self):
        return self.name


class CompletedEducationTasksManager(models.Manager):
    def get_comleted_tasks(self):
        return Tasks.objects.all().filter(status="completed")


class EducationTasks(Tasks):
    objects = CompletedEducationTasksManager()
    class Meta:
        proxy = True
        verbose_name = "Образовательная задача"
        verbose_name_plural = "Образовательные задачи"

    def __str__(self):
        return f"{self.name}"


@receiver(post_save, sender=Tasks)
def create_task_comment(instance, created, **kwargs):
    if created:
        instance.comments.create(message = "Task created")