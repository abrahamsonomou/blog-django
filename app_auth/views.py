from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from .forms import *
from django.contrib import messages
from django.contrib.auth import get_user_model

CustomUser=get_user_model()

# Create your views here.

def register_user(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']

            user = CustomUser.objects.create_user(email=email, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('login')
            else:
                messages.error(request, 'Creation de compte echouee')
                return render(request, 'pages/register.html', {'form': form})
        else:
            for field in form.errors:
                form[field].field.widget.attrs['class'] += ' is-invalid'
            return render(request, "pages/register.html", {"form": form})
    else:
        form = RegisterForm(request.POST)
    return render(request, "pages/register.html", {"form": form})


def login_user(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
            else:
                messages.error(request, "Autehtification echouee.")
                return render(request, "pages/login.html", {"form": form})
        else:
            for field in form.errors:
                form[field].field.widget.attrs['class'] += ' is-invalid'
            return render(request, "pages/login.html", {"form": form})
    else:
        form = LoginForm()
    return render(request, "pages/login.html", {"form": form})


def logout_user(request):
    logout(request)
    return redirect('index')


def forgot_password(request):
    return render(request, 'pages/forgot_password.html')