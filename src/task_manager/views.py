from django.shortcuts import render
from task_manager.models import Tasks, Comments
from account.models import User
from django.http import HttpResponse
# Create your views here.
def index(request):
    data = {"header": "Hello World", 'message': 'welcome to python' }
    return render(request, 'tasks/base.html', context=data)

def home(request):
    return render(request, 'tasks/home.html')

def tasks(request):
    context = { "tasks": Tasks.objects.select_related("assignee").prefetch_related("tags","comments").all()}
    return render(request, 'tasks/tasks.html', context=context)

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
