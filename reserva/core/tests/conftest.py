from contextlib import contextmanager

import pytest

from django.core.management import call_command


@pytest.fixture(scope="session")
def django_db_setup(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        call_command("loaddata", "nationalities.json")


@pytest.fixture
def client_with_session(client):
    @contextmanager
    def create_session(**data):
        session = client.session
        session.update(data)
        session.save()
        yield client

    return create_session
