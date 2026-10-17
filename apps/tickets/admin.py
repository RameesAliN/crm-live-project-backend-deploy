from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Ticket

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = (
    "id",
    "ticket_name",
    "priority",
    "ticket_status",
    "created_at",
    "updated_at",
    )

    
    list_filter = (
        "priority",
        "ticket_status",
        "created_at",
    )

    search_fields = (
        "ticket_name",
        "description",
    )

    ordering = ("-id",)
