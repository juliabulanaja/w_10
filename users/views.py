from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View
from django.contrib.auth import authenticate, login, logout
from .forms import RegisterForm, LoginForm
from django.contrib import messages


class Signup(View):

    def get(self, request):

        if request.user.is_authenticated:
            return redirect(to='quotes:main')

        form = RegisterForm()
        context = {
            "form": form,
        }
        return render(request, 'users/signup.html', context)

    def post(self, request):

        if not request.user.is_authenticated:
            return redirect(to='quotes:main')

        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse(666)

        context = {
            "form": form,
        }
        return render(request, 'users/signup.html', context)


class Signin(View):

    def get(self, request):

        if not request.user.is_authenticated:
            return redirect(to='quotes:main')

        form = LoginForm()
        context = {
            "form": form,
        }
        return render(request, 'users/signin.html', context)

    def post(self, request):

        if not request.user.is_authenticated:
            return redirect(to='quotes:main')

        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            form = LoginForm()
            messages.error(request, 'Username or password didn\'t match')
            return render(request, 'users/signin.html', {'form': form})


class Logout(View):

    def get(self, request):
        logout(request)
        return redirect(to='noteapp:main')

