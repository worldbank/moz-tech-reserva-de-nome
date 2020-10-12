from django.urls import path

from reserva.core.views import name_available, check_name, request_name, payment, request_performed, request_successful

app_name = "core"
urlpatterns = [
    path("name_available", name_available, name="name_available"),
    path("check_name", check_name, name="check_name"),
    path("request_name", request_name, name="request_name"),
    path("payment", payment, name="payment"),
    path("request_performed", request_performed, name="request_performed"),
    path("request_successful", request_successful, name="request_successful"),
]
