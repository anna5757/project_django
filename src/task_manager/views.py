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

def tasks(request):
    tasks_qs = Tasks.objects.select_related("assignee").prefetch_related(
        "tags",
        "comments",
        "attachments"
    ).all()
    paginator = Paginator(tasks_qs, 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {
        "tasks": page_obj,
        "page_obj": page_obj,
    }
    return render(request, "tasks/tasks.html", context=context)

def index(request):
    data = {"header": "Hello World", 'message': 'welcome to python' }
    return render(request, 'tasks/base.html', context=data)

def home(request):
    return render(request, 'tasks/home.html')

def users(request):
    context = {"users": User.objects.all()}
    return render(request, 'tasks/users.html', context=context)

def user_tasks(request, user_id):
    user = User.objects.get(id=user_id)
    tasks = Tasks.objects.filter(assignee=user)
    context={
        "tasks": tasks,
        "user": user
    }
    return render(request, 'tasks/user_tasks.html', context=context)

def add_comment_form(request):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            user_id = request.POST.get('user')
            task_id = request.POST.get('task')
            is_owner =Tasks.objects.filter(id = task_id, assignee_id = user_id).exists()
            if is_owner:
                Comments.objects.create(
                    message=form.cleaned_data['message'],
                    user=form.cleaned_data['user'],
                    task=form.cleaned_data['task']
                )
                return HttpResponseRedirect('/tasks/tasks')
            else:
                raise ValueError("Пользователь может оставить комментарий только к своей задаче")
    else:
        form = CommentForm()

    return render(request, "tasks/comment_form.html", {"form": form})

def add_task_form(request):
    if request.method == 'POST':
        form = TasksForm(request.POST)
        if form.is_valid():
            #import pdb; pdb.set_trace()
            #task = form.save(commit=False)
            #task.assignee = request.user
            form.save()
            return HttpResponseRedirect('/tasks/tasks')
    else:
        form = TasksForm()

    return render(request, "tasks/task_form.html", {"form": form})

def edit_task_form(request, task_id):
    task = Tasks.objects.get(id=task_id)
    if request.method == 'POST':
        form = TasksForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/tasks/tasks')
    else:
        form = TasksForm(instance=task)
    return render(request, "tasks/edit_task_form.html", {"form": form})


def add_tag_form(request):
    if request.method == 'POST':
        form = TagsForm(request.POST)
        if form.is_valid():
            tag = form.save(commit=False)
            tag.save()
            form.save_m2m()
            return HttpResponseRedirect('/tasks/tasks')
    else:
        form = TagsForm()
    return render(request, "tasks/add_tag.html", {"form": form})


def create_attachment(request):

    if request.method == "POST":

        form = AttachmentsForm(request.POST,request.FILES)

        if form.is_valid():

            form.save()
            return HttpResponseRedirect(reverse("tasks"))
    else:
        form = AttachmentsForm()

    return render(request, "tasks/create_attachment.html", {"form": form})


def add_attachment(request, task_id):
    task = Tasks.objects.get(id=task_id)
    file_path = r"C:\Users\Anna\Desktop\example.docx"
    attachment = add_attachment_from_external(
            task = task,
            name = "Документ",
            file_path = file_path
        )
    answer = f"Файл добавлен:{attachment.name}"
    return HttpResponse(answer)