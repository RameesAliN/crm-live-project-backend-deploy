from django.conf import settings
from django.db import models


class Meeting(models.Model):
    title = models.CharField(max_length=255)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    attendees = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="meetings",
    )

    location = models.CharField(max_length=255, blank=True)
    reminder = models.CharField(max_length=100, blank=True)
    note = models.TextField()

    lead = models.ForeignKey("leads.Lead", on_delete=models.CASCADE, null=True, blank=True, related_name="meetings")
    company = models.ForeignKey("companies.Company", on_delete=models.CASCADE, null=True, blank=True, related_name="meetings")
    deal = models.ForeignKey("deals.Deal", on_delete=models.CASCADE, null=True, blank=True, related_name="meetings")
    ticket = models.ForeignKey("tickets.Ticket", on_delete=models.CASCADE, null=True, blank=True, related_name="meetings")

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_meetings",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-start_time"]

    def __str__(self):
        return self.title