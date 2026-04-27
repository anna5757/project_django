from django.urls import path, include
from .views import (MyView, HomeMyTemplateView, TasksView, UserView, UserTasksView, TaskFormView,
                    TagFormView, CommentFormView,AttachmentFormView, EditTaskFormView, AddAttachmentView)
from task_manager import views

urlpatterns = [
    path("details/", MyView.as_view()),
    path('home', HomeMyTemplateView.as_view(), name='home'),
    path('tasks', TasksView.as_view(), name = 'tasks'),
    path('users', UserView.as_view(), name = 'users'),
    path('<int:user_id>', UserTasksView.as_view(), name = 'user_tasks'),
    path('add_comment', CommentFormView.as_view(), name='add_comment'),
    path('add_task', TaskFormView.as_view(), name='add_task'),
    path('edit_task/<int:pk>/', EditTaskFormView.as_view(), name='edit_task'),
    path('add_tag', TagFormView.as_view(), name='add_tag'),
    path("create_attachment",AttachmentFormView.as_view(),name="create_attachment"),
    path('task/<int:task_id>/add_attach_external/', AddAttachmentView.as_view(), name='add_attach_external'),
    path("api/", include("task_manager.v1.urls")),
]