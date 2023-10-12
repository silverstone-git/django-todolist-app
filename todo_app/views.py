from datetime import datetime
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from .models import Todo
from .forms import TodoForm, LoginForm
from django.contrib.auth.forms import UserCreationForm


# Create your views here.

def index(request):
    if not request.user.is_authenticated:
        return render(request, 'index.html', {'anonymous': True})

    user_todos = list(Todo.objects.filter(user = request.user))

    if request.method == "POST":
        # user is trying to post a todo, not view it
        form = TodoForm(request.POST)
        if form.is_valid():
            todo = form.save(commit = False)
            todo.user = request.user
            todo.added = datetime.now()
            todo.completed = None
            todo.save()

            # empty the form after saving
            form = TodoForm()
            messages.success(request, "Ban gya todo")
            return render(request, 'index.html', {'todos': user_todos + [todo], 'form': form, 'anonymous': False})
        else:
            # not emptying the form to let the user validate it
            messages.warning(request, "Nahi bana todo")
            return render(request, 'index.html', {'todos': user_todos, 'form': form, 'anonymous': False})
    #elif request.method == "UPDATE":
        # updates the todo by title
    #elif request.method == "DELETE":
        # Deletes the todo by title

    # get username and show their todos

    print("request user and todos are: ")
    print(request.user)
    print(user_todos)

    # form stuff
    form = TodoForm()
    return render(request, 'index.html', {'todos': user_todos, 'form': form, 'anonymous': False})


def signup(request):
    userform = UserCreationForm()
    if request.method == "POST":
        userform = UserCreationForm(request.POST)
        print("userform data is: ")
        print(userform.data)
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
            print("the request method was indeed post")
            login_req: dict[str, list[str]] = dict(request.POST)
            
            user = authenticate(username = form.data['username'][0].strip(), password = form.data['password'][0].strip())
            print("got user from authenticate function: \n", user)
            if user is not None:
                login(request, user)
                messages.success(request, "you are logged in")
                return redirect('/')
            else:
                messages.warning(request, "login fail")
        else:
            messages.warning(request, "form invalid")
    return render(request, 'auth.html', {'form': form})



def about(request):
    return render(request, 'about.html')
