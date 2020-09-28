import pytest

from reserva.core.models import NameApplication, Nationality


@pytest.mark.django_db
def test_name_application():
    obj = NameApplication.objects.create(
        name="minha empresa",
        applicant="meu nome",
        dob="1975-09-16",
        nationality=Nationality.objects.get(name="Moçambicano(a)"),
    )
    assert str(obj) == "minha empresa"
