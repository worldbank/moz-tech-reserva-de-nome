from django.dispatch import receiver
from django.db import models

from reserva.core.managers import NameApplicationManager, NationalityManager


class Nationality(models.Model):
    name = models.CharField("Nacionalidade", max_length=32)

    objects = NationalityManager()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "nacionalidade"
        ordering = ("name",)
        indexes = [models.Index(fields=["name"])]


class NameApplicationError(Exception):
    pass


class NameApplication(models.Model):
    name = models.CharField("Nome da empresa", max_length=256, unique=True)
    applicant = models.CharField("Responsável", max_length=256)
    dob = models.DateField("Data de nascimento")
    nationality = models.ForeignKey(
        "Nationality", verbose_name="Nacionalidade", on_delete=models.PROTECT
    )
    address1 = models.CharField(
        "Endereço (linha 1)", max_length=256, null=True, blank=True
    )
    address2 = models.CharField(
        "Endereço (linha 2)", max_length=256, null=True, blank=True
    )
    approved = models.BooleanField("Aprovado", default=False)
    approved_by = models.ForeignKey(
        "auth.User",
        verbose_name="Aprovado por",
        null=True,
        blank=True,
        on_delete=models.PROTECT,
    )
    comments = models.TextField("Comentários", null=True, blank=True)
    created_at = models.DateTimeField("Criado em", auto_now_add=True)
    updated_at = models.DateTimeField("Alterado em", auto_now=True)

    objects = NameApplicationManager()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "pedido de reserva de nome"
        verbose_name_plural = "pedidos de reserva de nome"
        ordering = ("-created_at", "name")
        indexes = [
            models.Index(fields=["created_at"]),
            models.Index(fields=["updated_at"]),
            models.Index(fields=["name"]),
            models.Index(fields=["approved"]),
            models.Index(fields=["approved_by"]),
        ]


@receiver(models.signals.pre_save, sender=NameApplication)
def manage_approved_by(sender, instance, **kwargs):
    if not instance.approved:
        instance.approved_by = None
        return instance

    if not instance.approved_by:
        msg = "Cannot approve application without user in `approved_by` field"
        raise NameApplicationError(msg)

    if not instance.approved_by.is_staff:
        raise NameApplicationError("Non-staff user cannot approve application.")

    return instance
