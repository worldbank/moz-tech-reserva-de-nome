from django.urls import reverse


def test_admin(client, admin_client):
    assert client.get(reverse("admin:index")).status_code == 302
    assert admin_client.get(reverse("admin:index")).status_code == 200
