from django.db import models

from reserva.core.hash_id import hash_id


class NameApplicationQuerySet(models.QuerySet):
    def is_available(self, name):
        return not self.filter(name__iexact=name).exists()

    def pending(self):
        return self.filter(status="P")  # TODO use constant wo/ cyclical import

    def from_hash_id(self, value):
        pk, *_ = hash_id.decode(value)
        return self.get(pk=pk)


class NationalityQuerySet(models.QuerySet):
    def default(self):
        return self.get(name="Moçambicano(a)")


NameApplicationManager = models.Manager.from_queryset(NameApplicationQuerySet)
NationalityManager = models.Manager.from_queryset(NationalityQuerySet)
