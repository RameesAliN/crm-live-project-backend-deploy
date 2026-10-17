from django.contrib import admin
from .models import Note


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = (
        "created_by",
        "id",
        "created_at",
        "updated_at",
    )

    search_fields = ("content",)
    list_filter = ("created_at",)
    ordering = ("-created_at",)
    readonly_fields = ("created_at", "updated_at")