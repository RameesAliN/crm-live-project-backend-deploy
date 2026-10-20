from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import CallActivity

@admin.register(CallActivity)
class CallActivityAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "lead",
        "call_outcome",
        "date",
        "time",
        "created_at",
    )

    list_filter = (
        "call_outcome",
        "date",
    )

    search_fields = (
        "lead__first_name",
        "lead__last_name",
        "lead__email",
        "note",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    ordering = ("-date", "-time")
