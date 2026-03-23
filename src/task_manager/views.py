from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
def index(request):
    data = {"header": "Hello World", 'message': 'welcome to python' }
    return render(request, 'tasks/base.html', context=data)

def home(request):
    return render(request, 'tasks/home.html')

def tasks(request):
    task = [
        {"task_name": "Fix login bug", "status": "in progress", "priority": "high"},
        {"task_name": "Create navbar", "status": "done", "priority": "medium"},
        {"task_name": "Write tests", "status": "todo", "priority": "high"},
        {"task_name": "Update documentation", "status": "todo", "priority": "low"},
        {"task_name": "Deploy project", "status": "in progress", "priority": "medium"}
    ]
    context = {"task": task}
    return render(request, 'tasks/tasks.html', context=context)

def users(request):
    users = [
        {"name": "Alice", "age": 25, "src": 'user_2.jpg'},
        {"name": "Bob", "age": 30, "src": 'user_1.jpg'},
        {"name": "Charlie", "age": 28, "src": 'user_4.jpg'},
        {"name": "Diana", "age": 22, "src": 'user_3.jpg'}
    ]
    context = {"users": users}
    return render(request, 'tasks/users.html', context=context)