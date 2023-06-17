from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .login import LoginForm


from .register import RegisterForm


def signupuser(request):
    if request.user.is_authenticated:
        return redirect(to="quote:main")

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            print('Try redirect')
            return redirect(to="quotes:root")
        else:
            return render(request, "users/signup.html", context={"form": form})

    return render(request, "users/signup.html", context={"form": RegisterForm()})


def signinuser(request):
    if request.user.is_authenticated:
        return redirect(to="quotes:root")

    if request.method == "POST":
        user = authenticate(
            username=request.POST["username"], password=request.POST["password"]
        )
        if user is None:
            messages.error(request, "Username or password didn't match")
            return redirect(to="users:signin")

        login(request, user)
        return redirect(to="quotes:root")

    return render(request, "users/login.html", context={"form": LoginForm()})
