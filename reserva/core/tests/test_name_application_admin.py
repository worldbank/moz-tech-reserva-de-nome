import pytest
from django.shortcuts import resolve_url
from mixer.backend.django import mixer

from reserva.core.models import NameApplication


@pytest.mark.django_db
def test_admin_injects_current_user_when_approving(admin_client, admin_user):
    obj = mixer.blend(NameApplication, approved=False)
    assert not obj.approved
    url = resolve_url("admin:core_nameapplication_change", object_id=obj.pk)
    admin_client.post(url, data={"approved": "on"})
    obj = NameApplication.objects.first()  # reload from the database
    assert obj.approved
    assert obj.approved_by == admin_user
