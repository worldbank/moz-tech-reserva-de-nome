from django.urls import path

from reserva.core.views import name_available

app_name = "core"
urlpatterns = [
    path("name_available", name_available, name="name_available"),
]
