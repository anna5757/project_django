from django.core.management.base import BaseCommand, CommandError
from task_manager.models import Tasks



class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        for ind in range(10):
            Tasks.objects.create(name=f"task{ind}")
            self.style.SUCCESS('Successfully created task')


