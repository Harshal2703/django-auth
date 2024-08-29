from django.shortcuts import render
from django.http import HttpResponse
from .forms import (
    RegistrationForm,
    SigninForm,
    ForgotPassForm,
    ResetPassForm,
    ChangePassForm,
)
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from .models import Unverified_User, Forgot_Pass, UserInfo
import uuid
from django.core.mail import send_mail
from django.shortcuts import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone


@login_required(login_url="signin")
def dashboard(request):
    user = request.user
    return render(request, "pages/home.html", {"username": user.username})


def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password2")
            key = uuid.uuid1()
            o = Unverified_User.objects.filter(unverified_username=username)
            if not o.exists():
                o = Unverified_User()
            else:
                o = Unverified_User.objects.get(unverified_username=username)
            o.unverified_username = username
            o.unverified_email = email
            o.unverified_password = password
            o.verifyKey = key
            print(username, email, password)
            o.save()
            send_mail(
                "Verify yourself",
                f"http://127.0.0.1:8000/verify?key={key}",
                "chessmate2023@outlook.com",
                [email],
                fail_silently=False,
            )
            return HttpResponse("visit the link sent to your email to verify yourself")
    else:
        form = RegistrationForm()
    return render(request, "auth/register.html", {"form": form})


def verify(request):
    key = request.GET.get("key")
    o = Unverified_User.objects.filter(verifyKey=key)
    if o.exists():
        o = Unverified_User.objects.get(verifyKey=key)
        if not User.objects.filter(email=o.unverified_email).exists():
            username = o.unverified_username
            email = o.unverified_email
            password = o.unverified_password
            user = User.objects.create_user(
                username=username, email=email, password=password
            )
            o1 = UserInfo()
            o1.email = email
            o1.save()
            login(request, user)
            o.delete()
            return HttpResponseRedirect("/dashboard")
    return HttpResponse("bad request")


def signout(request):
    logout(request)
    print("check")
    return HttpResponseRedirect("/login")


def signin(request):
    if request.method == "POST":
        form = SigninForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return HttpResponseRedirect("/dashboard")
            return HttpResponse("invalid credentials")
    form = SigninForm()
    return render(request, "auth/login.html", {"form": form})


def forgot_password(request):
    if request.method == "POST":
        form = ForgotPassForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            key = uuid.uuid1()
            if Forgot_Pass.objects.filter(email=email).exists():
                Forgot_Pass.objects.get(email=email).delete()
            o = Forgot_Pass()
            o.email = email
            o.verifyKey = key
            o.save()
            send_mail(
                "Verify yourself",
                f"http://127.0.0.1:8000/reset_password?key={key}",
                "chessmate2023@outlook.com",
                [email],
                fail_silently=False,
            )
            return HttpResponse("check your email to reset your password")
    form = ForgotPassForm()
    return render(request, "auth/forgot_pass.html", {"form": form})


def reset_password(request):
    if request.method == "GET":
        form = ResetPassForm()
        return render(request, "auth/reset_pass.html", {"form": form})
    elif request.method == "POST":
        key = request.GET.get("key")
        form = ResetPassForm(request.POST)
        if not form.is_valid():
            return HttpResponseRedirect("bad request")
        new_password = form.cleaned_data.get("password2")
        if Forgot_Pass.objects.filter(verifyKey=key).exists():
            o = Forgot_Pass.objects.get(verifyKey=key)
            email = o.email
            if User.objects.filter(email=email).exists():
                user = User.objects.get(email=email)
                user.set_password(new_password)
                user.save()
                o1 = UserInfo.objects.get(email=email)
                o1.last_updated = timezone.now()
                o1.save()
                return HttpResponse("password changed successfully!")
        return HttpResponse("bad request")


@login_required(login_url="signin")
def profile(request):
    user = request.user
    o = UserInfo.objects.get(email=user.email)
    return render(
        request,
        "pages/profile.html",
        {
            "username": user.username,
            "email": user.email,
            "date_joined": o.date_joined,
            "last_updated": o.last_updated,
        },
    )


@login_required(login_url="signin")
def change_password(request):
    if request.method == "GET":
        form = ChangePassForm()
        return render(request, "auth/change_pass.html", {"form": form})
    if request.method == "POST":
        form = ChangePassForm(request.POST)
        if not form.is_valid():
            return HttpResponseRedirect("bad request")
        old_password = form.cleaned_data.get("old_password")
        new_password = form.cleaned_data.get("new_password")
        user = request.user
        if user.check_password(old_password):
            user.set_password(new_password)
            o1 = UserInfo.objects.get(email=user.email)
            o1.last_updated = timezone.now()
            o1.save()
            user.save()
            return HttpResponse("password changed successfully!")
        return HttpResponse("invalid credentials!")
