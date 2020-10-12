from django.urls import path

from reserva.core.views.name_application import check, done, pay, send, success


app_name = "name_application"
urlpatterns = [
    path("check", check, name="check"),
    path("send", send, name="send"),
    path("pay", pay, name="pay"),
    path("done", done, name="done"),
    path("success", success, name="success"),
]
