from django.contrib import admin
from .models import Lead


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "first_name",
        "last_name",
        "email",
        "contact_owner_name",
    )

    @admin.display(description="Contact Owner")
    def contact_owner_name(self, obj):
        if obj.contact_owner:
            return (
                obj.contact_owner.first_name
                or obj.contact_owner.email
            )
        return "Unassigned"