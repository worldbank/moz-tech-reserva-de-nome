from django.urls import path

from reserva.core.views.api import available


app_name = "name_application_api"
urlpatterns = [
    path("available", available, name="available"),
]
