import pytest
from mixer.backend.django import mixer

from reserva.core.forms import CheckForm, PayForm, SendForm
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
        "applicant": "Meu Nome",
        "dob": "1970-01-01",
        "nationality": str(nationality),
        "email": "meu@no.me",
    }
    form = SendForm(data)
    assert form.is_valid()


@pytest.mark.django_db
def test_pay_form():
    name_application = mixer.blend(
        NameApplication, nationality=Nationality.objects.default()
    )
    data = {
        "name_application": str(name_application.pk),
        "name": "m nome",
        "number": "1234 1234 1234 1234",
        "expiry": "01/1970",
        "cvv": "123",
    }
    form = PayForm(data)
    assert form.is_valid()
    assert form.cleaned_data["name"] == "M NOME"
    assert form.cleaned_data["number"] == "1234123412341234"
    assert form.cleaned_data["cvv"] == 123
