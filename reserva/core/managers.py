from django.db import models


class NameApplicationQuerySet(models.QuerySet):
    def is_available(self, name):
        return not self.filter(name__iexact=name).exists()

    def pending(self):
        return self.filter(approved=False)


class NationalityQuerySet(models.QuerySet):
    def default(self):
        return self.get(name="Moçambicano(a)")


NameApplicationManager = models.Manager.from_queryset(NameApplicationQuerySet)
NationalityManager = models.Manager.from_queryset(NationalityQuerySet)
