from django.conf import settings
from django.db import models


class Email(models.Model):
    subject = models.CharField(max_length=255)
    body = models.TextField()
    recipient_email = models.EmailField()
    sent_at = models.DateTimeField(null=True, blank=True)
    cc = models.JSONField(default=list, blank=True)
    bcc = models.JSONField(default=list, blank=True)
    
    lead = models.ForeignKey(
        "leads.Lead",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="emails",
    )

    company = models.ForeignKey(
        "companies.Company",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="emails",
    )

    deal = models.ForeignKey(
        "deals.Deal",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="emails",
    )

    ticket = models.ForeignKey(
            "tickets.Ticket",
            on_delete=models.CASCADE,
            null=True,
            blank=True,
            related_name="emails",
        )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_emails",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject