import pytest
from django.urls import reverse
from mixer.backend.django import mixer

from reserva.core.models import NameApplication


@pytest.mark.django_db
@pytest.mark.parametrize(
    "lookup,expected", (("minha empresa", False), ("minha comapanhia", True))
)
def test_name_exists(client, lookup, expected):
    mixer.blend(NameApplication, name="minha empresa")
    response = client.post(reverse("api:name_available"), {"name": lookup})
    data = response.json()
    assert data["available"] is expected


@pytest.mark.django_db
def test_name_exists_is_case_insentive(client):
    mixer.blend(NameApplication, name="minha empresa")
    response = client.post(reverse("api:name_available"), {"name": "Minha Empresa"})
    data = response.json()
    assert data["available"] is False
