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
        owners = obj.contact_owner.all()
        if owners.exists():
            return ", ".join(owner.first_name or owner.email for owner in owners)
        return "Unassigned"