from asyncio import tasks

from django.urls import path
from .views import index, home, tasks, users
from task_manager import views

urlpatterns = [
    path('', index),
    path('home', home, name='home'),
    path('tasks', tasks, name = 'tasks'),
    path('users', users, name = 'users')
]
