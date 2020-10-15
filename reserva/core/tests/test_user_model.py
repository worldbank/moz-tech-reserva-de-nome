import pytest

from reserva.core.models import User


@pytest.mark.django_db
def test_user_name():
    user = User.objects.create_user("joanedoe", first_name="Joane", last_name="Doe")
    assert user.name == "Joane Doe"
    assert str(user) == user.name


@pytest.mark.django_db
def test_user_without_name():
    user = User.objects.create_user("joanedoe")
    assert user.name == ""
    assert str(user) == user.username


@pytest.mark.django_db
def test_user_without_last_name():
    user = User.objects.create_user("joanedoe", first_name="Joane")
    assert user.name == "Joane"
    assert str(user) == user.name
