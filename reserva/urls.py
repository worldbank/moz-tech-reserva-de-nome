from django.contrib import admin
from django.urls import include, path

from reserva.core.views.name_application import home


urlpatterns = [
    path("/", home, name="home"),
    path(
        "name_application/",
        include("reserva.core.urls.name_application", namespace="name_application"),
    ),
    path(
        "api/name_application/",
        include("reserva.core.urls.api", namespace="name_application_api"),
    ),
    path("admin/", admin.site.urls),
]
