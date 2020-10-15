import pytest

from django.conf import settings

from reserva.core.models import NameApplication, NameApplicationError, Nationality


@pytest.mark.django_db
def test_name_application():
    obj = NameApplication.objects.create(
        name="minha empresa",
        applicant="meu nome",
        dob="1975-09-16",
        nationality=Nationality.objects.get(name="Moçambicano(a)"),
        email="meu@no.me",
    )
    assert str(obj) == "minha empresa"
    assert obj.status == obj.PENDING
    assert isinstance(obj.hash_id, str)
    assert len(obj.hash_id) >= settings.HASH_ID_MIN_LENGTH
    assert obj == NameApplication.objects.from_hash_id(obj.hash_id)


@pytest.mark.django_db
def test_name_application_approval(admin_user):
    obj = NameApplication.objects.create(
        name="minha empresa",
        applicant="meu nome",
        dob="1975-09-16",
        nationality=Nationality.objects.get(name="Moçambicano(a)"),
        email="meu@no.me",
    )

    obj.status = obj.APPROVED
    obj.moderated_by = admin_user
    obj.comments = "belo nome"
    obj.save()
    assert obj.status == obj.APPROVED
    assert obj.moderated_by == admin_user
    assert obj.comments == "belo nome"


@pytest.mark.django_db
def test_faild_attempt_name_application_approval(django_user_model):
    user = django_user_model.objects.create(username="not", password="admin")
    obj = NameApplication.objects.create(
        name="minha empresa",
        applicant="meu nome",
        dob="1975-09-16",
        nationality=Nationality.objects.get(name="Moçambicano(a)"),
        email="meu@no.me",
    )

    obj.status = obj.APPROVED
    obj.moderated_by = user
    with pytest.raises(NameApplicationError) as error:
        obj.save()

    assert (
        error.value.args[0] == "Non-staff user cannot approve or reject applications."
    )
    obj = NameApplication.objects.first()  # reload from the database
    assert obj.status == obj.PENDING
    assert not obj.moderated_by


@pytest.mark.django_db
def test_faild_attempt_to_create_approved_name_application(django_user_model):
    with pytest.raises(NameApplicationError) as error:
        NameApplication.objects.create(
            name="minha empresa",
            applicant="meu nome",
            dob="1975-09-16",
            nationality=Nationality.objects.get(name="Moçambicano(a)"),
            email="meu@no.me",
            status=NameApplication.APPROVED,
        )
    expected = (
        "Cannot approve or reject application without user in `moderated_by` field"
    )
    assert error.value.args[0] == expected


@pytest.mark.django_db
def test_name_application_removed_approval(admin_user):
    obj = NameApplication.objects.create(
        name="minha empresa",
        applicant="meu nome",
        dob="1975-09-16",
        nationality=Nationality.objects.get(name="Moçambicano(a)"),
        email="meu@no.me",
        status=NameApplication.APPROVED,
        moderated_by=admin_user,
        comments="belo nome",
    )

    obj.status = obj.PENDING
    obj.rejected_by = admin_user
    obj.save()
    assert obj.status == obj.PENDING
    assert not obj.moderated_by
    assert obj.comments == "belo nome"


@pytest.mark.django_db
def test_is_available():
    NameApplication.objects.create(
        name="minha empresa",
        applicant="meu nome",
        dob="1975-09-16",
        nationality=Nationality.objects.get(name="Moçambicano(a)"),
        email="meu@no.me",
    )
    assert NameApplication.objects.is_available("minha empresa 2")
    assert not NameApplication.objects.is_available("Minha Empresa")
    assert not NameApplication.objects.is_available("minha empresa")


@pytest.mark.django_db
def test_pending(admin_user):
    assert not NameApplication.objects.pending().count()
    obj = NameApplication.objects.create(
        name="minha empresa",
        applicant="meu nome",
        dob="1975-09-16",
        nationality=Nationality.objects.get(name="Moçambicano(a)"),
        email="meu@no.me",
    )
    assert NameApplication.objects.pending().count() == 1

    obj.status = NameApplication.APPROVED
    obj.moderated_by = admin_user
    obj.comments = "belo nome"
    obj.save()
    assert not NameApplication.objects.pending().count()
