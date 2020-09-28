import pytest

from reserva.core.models import Nationality


@pytest.mark.django_db
def test_nationality():
    assert str(Nationality.objects.default()) == "Moçambicano(a)"
