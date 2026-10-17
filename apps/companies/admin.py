from django.contrib import admin
from .models import Company


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):

    list_display = (
        "company_name",
        "id",
        "display_company_owners",
        "industry",
        "type",
        "city",
        "created_date",
    )

    search_fields = (
        "company_name",
        "domain",
        "company_owner__first_name",
        "company_owner__last_name",
    )

    def display_company_owners(self, obj):
        return ", ".join(
            f"{user.first_name} {user.last_name}".strip()
            for user in obj.company_owner.all()
        )

    display_company_owners.short_description = "Company Owners"