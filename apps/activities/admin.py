from django.contrib import admin
from .models import Note,Task


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



@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        "task_name",
        "assigned_to",
        "priority",
        "status",
        "due_date",
        "id",
        "created_at",
        "updated_at",
    )
    search_fields = ("task_name", "note")
    list_filter = ("status","priority","task_type","created_at",)
    ordering = ("-created_at",)
    readonly_fields = ("created_at", "updated_at")