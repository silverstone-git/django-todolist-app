from datetime import datetime
from uuid import uuid4
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from .models import Todo
from .forms import TodoForm, LoginForm
from django.contrib.auth.forms import UserCreationForm


# Create your views here.

def index(request):
    if not request.user.is_authenticated:
        return render(request, 'index.html', {'anonymous': True})

    user_todos = Todo.objects.filter(user = request.user)
    form = TodoForm()
    if request.method == "POST" and request.POST.get("tobedeleted"):
        # user clicked the delete button
        user_todos.get(todoid=request.POST.get("tobedeleted")).delete()
        messages.success(request, "deleted todo!")
        return render(request, 'index.html', {'todos': user_todos, 'form': form, 'anonymous': False})
    elif request.method == "POST" and request.POST.get("tobeupdated"):
        # user clicked the checkbox
        print("request.POST in update block is ", request.POST)
        return render(request, 'index.html', {'todos': user_todos, 'form': form, 'anonymous': False})
    elif request.method == "POST" and request.POST.get("title") and request.POST.get("desc"):
        # user is trying to post a todo, not view it
        print("todo being added...")
        form = TodoForm(request.POST)
        if form.is_valid():
            todo = form.save(commit = False)
            todo.todoid = uuid4()
            print("new todo's todoid is : ", todo.todoid)
            todo.user = request.user
            todo.added = datetime.now()
            todo.completed = None
            todo.save()

            # empty the form after saving
            form = TodoForm()
            messages.success(request, "Ban gya todo")
            return render(request, 'index.html', {'todos': user_todos, 'form': form, 'anonymous': False})
        else:
            # not emptying the form to let the user validate it
            messages.warning(request, "Nahi bana todo")
            return render(request, 'index.html', {'todos': user_todos, 'form': form, 'anonymous': False})

    else:
        # get username and show their todos
        return render(request, 'index.html', {'todos': user_todos, 'form': form, 'anonymous': False})


def signup(request):
    userform = UserCreationForm()
    if request.method == "POST":
        userform = UserCreationForm(request.POST)
        if userform.is_valid():
            userform.save()
            userform = UserCreationForm()
            messages.success(request, "ban gaya user")
        else:
            messages.warning(request, "nahi bana user")
    return render(request, 'auth.html', {'form': userform})


def login_view(request):
    form = LoginForm()
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            login_req: dict[str, list[str]] = dict(request.POST)

            
            user = authenticate(request, username = form.data['username'].strip(), password = form.data['password'].strip())
            if user is not None:
                login(request, user)
                messages.success(request, "you are logged in")
                return redirect('/')
            else:
                messages.warning(request, "login fail")
        else:
            messages.warning(request, "form invalid")
    return render(request, 'auth.html', {'form': form})



def log_me_out(request):
    logout(request)
    messages.success(request, "You have been successfully logged out")
    return redirect("/")

def about(request):
    return render(request, 'about.html')
