from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin

from .forms import RegisterForm, LoginForm


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

        if request.user.is_authenticated:
            return redirect(to='quotes:main')

        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to='users:signin')

        context = {
            "form": form,
        }
        return render(request, 'users/signup.html', context)


class Signin(View):

    def get(self, request):

        if request.user.is_authenticated:
            return redirect(to='quotes:main')

        form = LoginForm()
        context = {
            "form": form,
        }
        return render(request, 'users/signin.html', context)

    def post(self, request):

        if request.user.is_authenticated:
            return redirect(to='quotes:main')

        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            print("no error")
            login(request, user)
            return redirect('/')
        else:
            form = LoginForm()
            messages.error(request, 'Username or password didn\'t match')
            print("error!!!!")
            return render(request, 'users/signin.html', {'form': form})


class Logout(View):

    def get(self, request):
        logout(request)
        return redirect(to='quotes:main')


class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'users/password_reset.html'
    email_template_name = 'users/password_reset_email.html'
    html_email_template_name = 'users/password_reset_email.html'
    success_url = reverse_lazy('users:password_reset_done')
    success_message = "An email with instructions to reset your password has been sent to %(email)s."
    subject_template_name = 'users/password_reset_subject.txt'

