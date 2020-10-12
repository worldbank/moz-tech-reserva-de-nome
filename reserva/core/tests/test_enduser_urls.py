from django.urls import reverse
from pytest_django.asserts import assertRedirects as assert_redirects


def test_home(client):
    response = client.get(reverse("home"))
    assert_redirects(response, reverse("name_application:check"))


def test_check(client):
    response = client.get(reverse("name_application:check"))
    assert response.status_code == 200


def test_send(client):
    response = client.get(reverse("name_application:send"))
    assert response.status_code == 200


def test_pay(client):
    response = client.get(reverse("name_application:pay"))
    assert response.status_code == 200


def test_done(client):
    response = client.get(reverse("name_application:done"))
    assert response.status_code == 200


def test_success(client):
    response = client.get(reverse("name_application:success"))
    assert response.status_code == 200
