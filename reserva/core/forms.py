from django import forms
from django.core.exceptions import ValidationError

from reserva.core.models import NameApplication


def get_name_max_length():
    for field in NameApplication._meta.fields:
        if field.name != "name":
            continue
        return field.max_length


class CheckForm(forms.Form):
    name = forms.CharField(
        label="Confira se o nome está disponível", max_length=get_name_max_length()
    )

    def clean_name(self):
        name = self.cleaned_data.get("name")
        if not NameApplication.objects.is_available(name):
            raise ValidationError("Nome indisponível.", "name_is_not_available")
        return name


class SendForm(forms.ModelForm):
    class Meta:
        model = NameApplication
        fields = ("name", "applicant", "dob", "nationality", "address1", "address2")
