import re

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
        fields = ("applicant", "dob", "nationality", "email")


class PayForm(forms.Form):
    name = forms.CharField(label="Nome como consta no cartão")
    number = forms.CharField(label="Número do cartão")
    expiry = forms.CharField(label="Data de validade")
    cvv = forms.IntegerField(label="Código de segurança", min_value=100, max_value=999)

    def clean_name(self):
        return self.cleaned_data.get("name").upper()

    def clean_number(self):
        cleaned = re.sub(r"\D", "", self.cleaned_data.get("number"))
        if len(cleaned) != 16:
            raise ValidationError("Número inválido.", "number_is_not_valid")
        return cleaned
