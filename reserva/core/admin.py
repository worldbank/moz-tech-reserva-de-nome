from django.contrib import admin

from reserva.core.models import NameApplication, User


class UsersWithApprovals(admin.SimpleListFilter):
    title = "Aprovado por"
    parameter_name = "approved_by"

    def lookups(self, request, model_admin):
        qs = User.objects.filter(
            pk__in=NameApplication.objects.exclude(approved_by=None)
            .values("approved_by__pk")
            .distinct()
        )
        return tuple((user.pk, user.name) for user in qs)

    def queryset(self, request, queryset):
        if not self.value():
            return queryset

        return queryset.filter(approved_by=self.value())


class NameApplicationModelAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "applicant",
        "approved",
        "approved_by",
        "created_at",
        "updated_at",
    )
    readonly_fields = (
        "name",
        "applicant",
        "dob",
        "nationality",
        "email",
        "approved_by",
        "created_at",
        "updated_at",
    )
    list_filter = ("approved", UsersWithApprovals, "created_at", "updated_at")

    def save_model(self, request, obj, form, change):
        if obj.approved:
            obj.approved_by = request.user
        super(NameApplicationModelAdmin, self).save_model(request, obj, form, change)


admin.site.register(NameApplication, NameApplicationModelAdmin)
