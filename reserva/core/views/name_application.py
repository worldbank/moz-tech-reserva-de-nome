from django.shortcuts import redirect, render
from django.urls import reverse


def home(request):
    return redirect(reverse("name_application:check"))


def check(request):
    return render(request, "name_application/check.html")


def send(request):
    return render(request, "name_application/send.html")


def pay(request):
    return render(request, "name_application/pay.html")


def done(request):
    return render(request, "name_application/done.html")


def success(request):
    return render(request, "name_application/success.html")
