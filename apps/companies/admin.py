from django.contrib import admin
from .models import Company


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "company_name",
        "company_owner",
        "industry",
        "city",
        "country_region",
        "created_date",
    )

    search_fields = (
        "company_name",
        "domain",
        "city",
    )

    list_filter = (
        "industry",
        "country_region",
    )

    ordering = ("-created_date",)