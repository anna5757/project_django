from asyncio import tasks

from django.urls import path
from .views import index, home, tasks, users, user_tasks
from task_manager import views

urlpatterns = [
    path('', index),
    path('home', home, name='home'),
    path('tasks', tasks, name = 'tasks'),
    path('users', users, name = 'users'),
    path('<int:user_id>', user_tasks, name = 'user_tasks'),
]