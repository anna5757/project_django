from django.urls import path

from task_manager.v1.views.comments import CommentApiView
from task_manager.v1.views.task import TaskListApiView, TaskDetailApiView
from task_manager.v1.views.tags import TagsApiView
from task_manager.v1.views.project import ProjectsApiView, ProjectDetailApiView
from task_manager.v1.views.attachments import AttachmentApiView
from task_manager.v1.views.projects_details import ProjectsDetailsApiView

urlpatterns = [
    path("tasks/", TaskListApiView.as_view()),
    path("tasks/<int:pk>/", TaskDetailApiView.as_view()),

    path('comments/', CommentApiView.as_view()),
    path("comments/<int:pk>/", CommentApiView.as_view()),

    path("tags/", TagsApiView.as_view()),
    path("tags/<int:pk>/", TagsApiView.as_view()),

    path("projects/", ProjectsApiView.as_view()),
    path("projects/<int:pk>/", ProjectDetailApiView.as_view()),

    path("attachments/", AttachmentApiView.as_view()),
    path("attachments/<int:pk>/", AttachmentApiView.as_view()),

    path("details/", ProjectsDetailsApiView.as_view()),
    path("attachments/<int:pk>/", ProjectsDetailsApiView.as_view()),

]