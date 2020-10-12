import pytest
from mixer.backend.django import mixer

from reserva.core.forms import CheckForm
from reserva.core.models import NameApplication


@pytest.mark.django_db
def test_check_form_success():
    form = CheckForm({"name": "Minha Empresa"})
    assert form.is_valid()


@pytest.mark.django_db
def test_check_form_fail():
    mixer.blend(NameApplication, name="Minha Empresa")
    form = CheckForm({"name": "Minha Empresa"})
    assert not form.is_valid()
