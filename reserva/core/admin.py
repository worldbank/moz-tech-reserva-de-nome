from django.contrib import admin

from reserva.core.models import NameApplication


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
        "address1",
        "address2",
        "approved_by",
        "created_at",
        "updated_at",
    )
    list_filter = ("approved", "approved_by", "created_at", "updated_at")

    def save_model(self, request, obj, form, change):
        if obj.approved:
            obj.approved_by = request.user
        super(NameApplicationModelAdmin, self).save_model(request, obj, form, change)


admin.site.register(NameApplication, NameApplicationModelAdmin)
