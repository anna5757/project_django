from django.urls import path
from task_manager.v1.views.task import TaskListApiView, TaskDetailApiView

urlpatterns = [
    path("tasks/", TaskListApiView.as_view()),
    path("tasks/<int:pk>/", TaskDetailApiView.as_view()),
]