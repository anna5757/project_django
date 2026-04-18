from django.urls import path
from .views import (index, home, tasks, users, user_tasks, add_comment_form, add_task_form, edit_task_form, add_tag_form,
create_attachment, add_attachment)
from task_manager import views

urlpatterns = [
    path('', index),
    path('home', home, name='home'),
    path('tasks', tasks, name = 'tasks'),
    path('users', users, name = 'users'),
    path('<int:user_id>', user_tasks, name = 'user_tasks'),
    path('add_comment', add_comment_form, name='add_comment'),
    path('add_task', add_task_form, name='add_task'),
    path('edit_task/<int:task_id>/', edit_task_form, name='edit_task'),
    path('add_tag', add_tag_form, name='add_tag'),
    path("create_attachment",create_attachment,name="create_attachment"),
    path('task/<int:task_id>/add_attach_external/', add_attachment, name='add_attach_external'),
]