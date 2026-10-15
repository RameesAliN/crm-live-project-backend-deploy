from django.db import models
from django.conf import settings

# Create your models here.
class Deal(models.Model):

    STAGE_CHOICES = [
        ("proposal_sent", "Proposal Sent"),
        ("negotiation", "Negotiation"),
        ("closed_won", "Closed Won"),
        ("closed_lost", "Closed Lost"),
    ]

    PRIORITY_CHOICES = [
        ("low", "Low"),
        ("medium", "Medium"),
        ("high", "High"),
    ]

    deal_name = models.CharField(max_length=200)

    associated_lead = models.ForeignKey(
        "leads.Lead",
        null=True,
        on_delete=models.SET_NULL,
        related_name="deals",
    )
    
    stage = models.CharField(max_length=30, choices=STAGE_CHOICES)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES)
    close_date = models.DateField()

    owners = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="deals",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.deal_name