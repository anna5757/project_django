from django.db import models
from config.models import BaseModel
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.utils.html import format_html

class Attachments(BaseModel):
    name = models.CharField(
        max_length=64,
        unique=True,
        verbose_name="Наименование"
    )
    task = models.ForeignKey(
        to="Tasks",
        related_name="attachments",
        on_delete=models.CASCADE
    )
    file = models.FileField(
        upload_to="attachments",
        blank=True,
        null=True,
        verbose_name="Файл"
    )
    photo = models.FileField(
        upload_to="attachments",
        blank=True,
        null=True,
        verbose_name="Фото"
    )

    class Meta:
        ordering = ["name"]
        db_table = "attachments"
        verbose_name = "Вложение"
        verbose_name_plural = "Вложения"


    def __str__(self):
        return self.name

    def secure_view(self):
        if self.file:
            return format_html(
                '<a href="{}" target="_blank">Открыть файл</a>',
                self.file.url
            )
        return "Нет файла"
    secure_view.short_description = "Файл"


@receiver(post_delete, sender=Attachments)
def delete_file(sender, instance, **kwargs):
    instance.file.delete(False)
#ПОЧЕМУ FALSE УДАЛЯЕТ ЗАПИСЬ ИЗ БД, А НЕ TRUE