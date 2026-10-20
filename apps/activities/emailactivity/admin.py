from django.contrib import admin
from .models import Email


@admin.register(Email)
class EmailAdmin(admin.ModelAdmin):
    list_display = (
        "subject",
        "created_by",
        "id",
        "created_at",
        "updated_at",
    )

    search_fields = ("subject", "recipient_email")
    list_filter = ("created_at",)
    ordering = ("-created_at",)
    readonly_fields = ("created_at", "updated_at")