from django.contrib import admin

from reserva.core.models import NameApplication, User


class UsersWithApprovals(admin.SimpleListFilter):
    title = "Aprovado por"
    parameter_name = "moderated_by"

    def lookups(self, request, model_admin):
        qs = User.objects.filter(
            pk__in=NameApplication.objects.exclude(moderated_by=None)
            .values("moderated_by__pk")
            .distinct()
        )
        return tuple((user.pk, user.name) for user in qs)

    def queryset(self, request, queryset):
        if not self.value():
            return queryset

        return queryset.filter(moderated_by=self.value())


class NameApplicationModelAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "applicant",
        "status",
        "moderated_by",
        "created_at",
        "updated_at",
    )
    readonly_fields = (
        "name",
        "applicant",
        "dob",
        "nationality",
        "email",
        "moderated_by",
        "created_at",
        "updated_at",
    )
    list_filter = ("status", UsersWithApprovals, "created_at", "updated_at")

    def save_model(self, request, obj, form, change):
        if obj.status in {NameApplication.APPROVED, NameApplication.REJECTED}:
            obj.moderated_by = request.user
        super(NameApplicationModelAdmin, self).save_model(request, obj, form, change)


admin.site.register(NameApplication, NameApplicationModelAdmin)
