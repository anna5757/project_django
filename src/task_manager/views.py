from django.shortcuts import render
from task_manager.models import Tasks, Comments, Attachments
from account.models import User
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from task_manager.forms import CommentForm, TasksForm, TagsForm, AttachmentsForm
from django.urls import reverse

from django.shortcuts import get_object_or_404
from task_manager.add_attachment_from_exernal_path import add_attachment_from_external
from django.core.paginator import Paginator

from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.core.cache import caches

from django.views import View
from django.views.generic import TemplateView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from django.views.generic.edit import UpdateView
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.urls import reverse_lazy
# def index_2(request):
#     return HttpResponse(f"<h1>Hello World!</h1>")

class MyView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse(f"<h1>Hello World!</h1>")

class HomeMyTemplateView(TemplateView):
    template_name = "tasks/home.html"
#@cache_page(1800)
# def tasks(request):
#     # import time
#     # time.sleep(3)
#     tasks_qs = Tasks.objects.select_related("assignee").prefetch_related(
#         "tags",
#         "comments",
#         "attachments"
#     ).all()
#     paginator = Paginator(tasks_qs, 5)
#     page_number = request.GET.get("page")
#     page_obj = paginator.get_page(page_number)
#     context = {
#         "tasks": page_obj,
#         "page_obj": page_obj,
#     }
#     return render(request, "tasks/tasks.html", context=context)
# @method_decorator(cache_page(60 * 10),name='dispatch')
class TasksView(ListView):
#class TasksView(PermissionRequiredMixin,LoginRequiredMixin,ListView):
    template_name = "tasks/tasks.html"
    #login_url = "/account/login/"
    #permission_required = 'task_manager.view_tasks'
    model = Tasks
    paginate_by = 5
    paginator_class = Paginator
    queryset = Tasks.objects.select_related("assignee").prefetch_related(
         "tags",
         "comments",
         "attachments"
     ).all()

    def get_context_data(self, **kwargs):
        context = super(TasksView, self).get_context_data(**kwargs)
        page_number = self.request.GET.get(self.page_kwarg)
        paginator = self.paginator_class(self.queryset, self.paginate_by)
        context["tasks"] = paginator.get_page(page_number)
        context["page_obj"] = paginator.get_page(page_number)
        return context

class UserView(ListView):
    model = User
    template_name = 'tasks/users.html'
    context_object_name = 'users'
# def user_tasks(request, user_id):
#     user = User.objects.get(id=user_id)
#     tasks = Tasks.objects.filter(assignee=user)
#
#     return render(request, "tasks/user_tasks.html", {
#         "tasks": tasks,
#         "user": user
#     })
class UserTasksView(ListView):
    model = Tasks
    template_name = 'tasks/user_tasks.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        user_id = self.kwargs["user_id"]
        return Tasks.objects.filter(assignee_id=user_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_id = self.kwargs["user_id"]
        context["user"] = User.objects.get(id=user_id)
        return context

#@cache_page(1800)
# def add_comment_form(request):
#     if request.method == 'POST':
#         form = CommentForm(request.POST)
#         if form.is_valid():
#             user_id = request.POST.get('user')
#             task_id = request.POST.get('task')
#             is_owner =Tasks.objects.filter(id = task_id, assignee_id = user_id).exists()
#             if is_owner:
#                 Comments.objects.create(
#                     message=form.cleaned_data['message'],
#                     user=form.cleaned_data['user'],
#                     task=form.cleaned_data['task']
#                 )
#                 #caches["default"].clear()
#                 return HttpResponseRedirect('/tasks/tasks')
#             else:
#                 raise ValueError("Пользователь может оставить комментарий только к своей задаче")
#     else:
#         form = CommentForm()
#     return render(request, "tasks/comment_form.html", {"form": form})
class CommentFormView(CreateView):
    template_name = "tasks/comment_form.html"
    form_class = CommentForm
    success_url ='/tasks/tasks'

    def form_valid(self, form):
        user_id = form.cleaned_data["user"].id
        task_id = form.cleaned_data["task"].id
        is_owner = Tasks.objects.filter(id=task_id,assignee_id=user_id).exists()
        if not is_owner:
            raise ValueError("Пользователь может оставить комментарий только к своей задаче")
        return super().form_valid(form)
# def add_task_form(request):
#     if request.method == 'POST':
#         form = TasksForm(request.POST)
#         if form.is_valid():
#             #import pdb; pdb.set_trace()
#             #task = form.save(commit=False)
#             #task.assignee = request.user
#             form.save()
#             #caches["default"].clear()
#             return HttpResponseRedirect('/tasks/tasks')
#     else:
#         form = TasksForm()
#
#     return render(request, "tasks/task_form.html", {"form": form})
class TaskFormView(CreateView):
    template_name = "tasks/task_form.html"
    form_class = TasksForm
    success_url ='/tasks/tasks'

class TagFormView(CreateView):
    template_name = "tasks/add_tag.html"
    form_class = TagsForm
    success_url ='/tasks/tasks'


class AttachmentFormView(CreateView):
    template_name = "tasks/create_attachment.html"
    form_class = AttachmentsForm
    success_url ='/tasks/tasks'

# def edit_task_form(request, task_id):
#     task = Tasks.objects.get(id=task_id)
#     if request.method == 'POST':
#         form = TasksForm(request.POST, instance=task)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect('/tasks/tasks')
#     else:
#         form = TasksForm(instance=task)
#     return render(request, "tasks/edit_task_form.html", {"form": form})
class EditTaskFormView(UpdateView):
    template_name = "tasks/edit_task_form.html"
    form_class = TasksForm
    model = Tasks
    success_url = '/tasks/tasks'


class AddAttachmentView(View):
    def get(self, request, task_id):
        task = Tasks.objects.get(id=task_id)
        file_path = r"C:\Users\Anna\Desktop\example.docx"
        attachment = add_attachment_from_external(
            task = task,
            name = "Документ",
            file_path = file_path
        )
        answer = f"Файл добавлен:{attachment.name}"
        return HttpResponse(answer)
