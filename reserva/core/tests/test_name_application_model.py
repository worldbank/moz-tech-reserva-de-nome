import pytest

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
    assert not obj.approved


@pytest.mark.django_db
def test_name_application_approval(admin_user):
    obj = NameApplication.objects.create(
        name="minha empresa",
        applicant="meu nome",
        dob="1975-09-16",
        nationality=Nationality.objects.get(name="Moçambicano(a)"),
        email="meu@no.me",
    )

    obj.approved = True
    obj.approved_by = admin_user
    obj.comments = "belo nome"
    obj.save()
    assert obj.approved
    assert obj.approved_by == admin_user
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

    obj.approved = True
    obj.approved_by = user
    with pytest.raises(NameApplicationError) as error:
        obj.save()

    obj = NameApplication.objects.first()  # reload form the database
    assert error.value.args[0] == "Non-staff user cannot approve application."
    assert not obj.approved
    assert not obj.approved_by


@pytest.mark.django_db
def test_faild_attempt_to_create_approved_name_application(django_user_model):
    with pytest.raises(NameApplicationError) as error:
        NameApplication.objects.create(
            name="minha empresa",
            applicant="meu nome",
            dob="1975-09-16",
            nationality=Nationality.objects.get(name="Moçambicano(a)"),
            email="meu@no.me",
            approved=True,
        )
    expected = "Cannot approve application without user in `approved_by` field"
    assert error.value.args[0] == expected


@pytest.mark.django_db
def test_name_application_removed_approval(admin_user):
    obj = NameApplication.objects.create(
        name="minha empresa",
        applicant="meu nome",
        dob="1975-09-16",
        nationality=Nationality.objects.get(name="Moçambicano(a)"),
        email="meu@no.me",
        approved=True,
        approved_by=admin_user,
        comments="belo nome",
    )

    obj.approved = False
    obj.save()
    assert not obj.approved
    assert not obj.approved_by
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

    obj.approved = True
    obj.approved_by = admin_user
    obj.comments = "belo nome"
    obj.save()
    assert not NameApplication.objects.pending().count()
