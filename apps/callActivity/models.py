from django.db import models
from django.conf import settings

from apps.leads.models import Lead
from apps.companies.models import Company
from apps.deals.models import Deal
from apps.tickets.models import Ticket


class CallActivity(models.Model):

    CALL_OUTCOME_CHOICES = [
        ("connected", "Connected"),
        ("notconnected", "Not Connected"),
        ("wrongnumber", "Wrong Number"),
        ("leftvoicemail", "Left Voicemail"),
    ]

    lead = models.ForeignKey(
        Lead,
        on_delete=models.CASCADE,
        related_name="call_activities",
        null=True,
        blank=True,
    )

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="call_activities",
        null=True,
        blank=True,
    )

    deal = models.ForeignKey(
        Deal,
        on_delete=models.CASCADE,
        related_name="call_activities",
        null=True,
        blank=True,
    )

    ticket = models.ForeignKey(
        Ticket,
        on_delete=models.CASCADE,
        related_name="call_activities",
        null=True,
        blank=True,
    )

    call_outcome = models.CharField(
        max_length=20,
        choices=CALL_OUTCOME_CHOICES,
    )

    date = models.DateField()

    time = models.TimeField()

    duration = models.PositiveIntegerField(
        default=0,
        help_text="Call duration in seconds",
    )

    note = models.TextField(blank=True, null=True)

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_call_activities",
    )

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-date", "-time"]

    def __str__(self):
        return f"Call {self.id} - {self.call_outcome}"