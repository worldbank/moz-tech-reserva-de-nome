import pytest
from django.urls import reverse
from pytest_django.asserts import assertRedirects as assert_redirects

from reserva.core.models import NameApplication, Nationality


def test_home(client):
    response = client.get(reverse("home"))
    assert_redirects(response, reverse("name_application:check"))


def test_get_check(client):
    response = client.get(reverse("name_application:check"))
    assert response.status_code == 200
    assert "Confira se o nome está disponível" in response.content.decode("utf8")


@pytest.mark.django_db
def test_post_check_with_error(client):
    response = client.post(reverse("name_application:check"), {"name": ""})
    assert response.status_code == 200  # TODO assert error message is in HTML


@pytest.mark.django_db
def test_post_check(client):
    response = client.post(reverse("name_application:check"), {"name": "Minha Empresa"})
    assert_redirects(response, reverse("name_application:send"))


@pytest.mark.django_db
def test_get_send(client_with_session):
    form = {"name": "Minha Empresa"}
    with client_with_session(form=form) as client:
        response = client.get(reverse("name_application:send"))

    assert response.status_code == 200
    assert "Responsável" in response.content.decode("utf8")
    assert "Data de nascimento" in response.content.decode("utf8")
    assert "Nacionalidade" in response.content.decode("utf8")
    assert "E-mail" in response.content.decode("utf8")


@pytest.mark.django_db
def test_post_send_with_error(client_with_session):
    form = {"name": "Minha Empresa"}
    with client_with_session(form=form) as client:
        form.update(
            {
                "applicant": "X",
                "dob": "123",
                "nationality": 9999,
                "email": "not an email",
            }
        )
        response = client.post(reverse("name_application:send"), form)
    assert response.status_code == 200  # TODO assert error message is in HTML


@pytest.mark.django_db
def test_post_send(client_with_session):
    form = {"name": "Minha Empresa"}
    with client_with_session(form=form) as client:
        form.update(
            {
                "applicant": "Meu Nome",
                "dob": "1970-01-01",
                "nationality": str(Nationality.objects.default().pk),
                "email": "meu@no.me",
            }
        )
        response = client.post(reverse("name_application:send"), form)

    assert_redirects(response, reverse("name_application:pay"))


@pytest.mark.django_db
def test_get_pay(client_with_session):
    form = {
        "name": "Minha Empresa",
        "applicant": "Meu Nome",
        "dob": "1970-01-01",
        "nationality": str(Nationality.objects.default().pk),
        "email": "meu@no.me",
    }
    with client_with_session(form=form) as client:
        response = client.get(reverse("name_application:pay"))

    assert response.status_code == 200
    assert "Nome como consta no cartão" in response.content.decode("utf8")
    assert "Número do cartão" in response.content.decode("utf8")
    assert "Data de validade" in response.content.decode("utf8")
    assert "Código de segurança" in response.content.decode("utf8")


@pytest.mark.django_db
def test_post_pay_with_error(client_with_session):
    form = {
        "name": "Minha Empresa",
        "applicant": "Meu Nome",
        "dob": "1970-01-01",
        "nationality": str(Nationality.objects.default().pk),
        "email": "meu@no.me",
    }
    data = {
        "name": "",
        "number": "1234",
        "expiry": "01/1970",
        "cvv": "123",
    }
    with client_with_session(form=form) as client:
        response = client.post(reverse("name_application:pay"), data)

    assert response.status_code == 200  # TODO assert error message is in HTML


@pytest.mark.django_db
def test_post_pay(client_with_session):
    form = {
        "name": "Minha Empresa",
        "applicant": "Meu Nome",
        "dob": "1970-01-01",
        "nationality": str(Nationality.objects.default().pk),
        "email": "meu@no.me",
    }
    data = {
        "name": "m nome",
        "number": "1234 1234 1234 1234",
        "expiry": "01/1970",
        "cvv": "123",
    }
    with client_with_session(form=form) as client:
        response = client.post(reverse("name_application:pay"), data)

    assert_redirects(response, reverse("name_application:done"))


@pytest.mark.django_db
def test_get_done_with_session(client_with_session):
    form = {
        "name": "Minha Empresa",
        "applicant": "Meu Nome",
        "dob": "1970-01-01",
        "nationality": str(Nationality.objects.default().pk),
        "email": "meu@no.me",
    }
    with client_with_session(form=form) as client:
        response = client.get(reverse("name_application:done"))

    assert NameApplication.objects.count() == 1
    assert response.status_code == 200
    assert "Minha Empresa" in response.content.decode("utf8")
    assert NameApplication.objects.first().hash_id in response.content.decode("utf8")


def test_get_done_without_session(client):
    response = client.get(reverse("name_application:done"))
    assert response.status_code == 404


@pytest.mark.django_db
@pytest.mark.parametrize("name", ("send", "pay", "done"))
def test_views_without_session(client, name):
    response = client.get(reverse(f"name_application:{name}"))
    assert response.status_code == 404


@pytest.mark.django_db
@pytest.mark.parametrize("name", ("pay", "done"))
def test_views_with_incomplete_session(client_with_session, name):
    form = {"name": "Minha Empresa"}
    with client_with_session(form=form) as client:
        response = client.get(reverse(f"name_application:{name}"))
    assert response.status_code == 404


def test_success(client):
    response = client.get(reverse("name_application:success"))
    assert response.status_code == 200
