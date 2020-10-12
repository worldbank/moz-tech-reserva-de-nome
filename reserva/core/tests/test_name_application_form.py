import pytest
from mixer.backend.django import mixer

from reserva.core.forms import CheckForm, SendForm
from reserva.core.models import NameApplication, Nationality


@pytest.mark.django_db
def test_check_form_success():
    form = CheckForm({"name": "Minha Empresa"})
    assert form.is_valid()


@pytest.mark.django_db
def test_check_form_fail():
    mixer.blend(NameApplication, name="Minha Empresa")
    form = CheckForm({"name": "Minha Empresa"})
    assert not form.is_valid()


@pytest.mark.django_db
def test_send_form():
    nationality = Nationality.objects.default().pk
    data = {
        "name": "Minha Empresa",
        "applicant": "Meu Nome",
        "dob": "1970-01-01",
        "nationality": str(nationality),
        "address1": "Rua 4",
        "address2": "Maputo",
    }
    form = SendForm(data)
    assert form.is_valid()
