from django.db import models
from django.conf import settings

# Create your models here.

class Attachment(models.Model):
    file = models.FileField(upload_to="attachments/%Y/%m/")
    original_name = models.CharField(max_length=255, blank=True)

    lead = models.ForeignKey(
            "leads.Lead",
            on_delete=models.CASCADE,
            null=True,
            blank=True,
            related_name="attachments",
        )
    
    company = models.ForeignKey(
        "companies.Company",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="attachments",
    )
    
    deal = models.ForeignKey(
        "deals.Deal",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="attachments",
    )
    
    ticket = models.ForeignKey(
        "tickets.Ticket",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="attachments",
    )

    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="uploaded_attachments",
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.original_name or self.file.name