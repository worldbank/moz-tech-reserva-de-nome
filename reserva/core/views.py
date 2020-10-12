from django.http import JsonResponse
from django.shortcuts import render

from reserva.core.models import NameApplication as NameApp


def name_available(request):
    return JsonResponse(
        {
            "available": NameApp.objects.is_available(request.POST["name"]),
            "name": request.POST["name"],
        }
    )

def check_name(request):
    return render(request, "check_name.html")

def request_name(request):
    return render(request, "request_name.html")

def payment(request):
    return render(request, "payment.html")

def request_performed(request):
    return render(request, "request_performed.html")

def request_successful(request):
    return render(request, "request_successful.html")
