

# Create your models here.
from django.db import models
from django.conf import settings

class Ticket(models.Model):


    STATUS_CHOICES = [
        ("New", "New"),
        ("Waiting on contact", "Waiting on contact"),
        ("Waiting on us", "Waiting on us"),
        ("Closed", "Closed"),
    ]

    SOURCE_CHOICES = [
        ("Chat", "Chat"),
        ("Email", "Email"),
        ("Phone", "Phone"),
    ]

    PRIORITY_CHOICES = [
        ("Critical", "Critical"),
        ("High", "High"),
        ("Medium", "Medium"),
        ("Low", "Low"),
    ]

    ticket_name = models.CharField(max_length=200)

    description = models.TextField(blank=True)

    ticket_status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default="New",
    )

    source = models.CharField(
        max_length=20,
        choices=SOURCE_CHOICES,
    )

    priority = models.CharField(
        max_length=10,
        choices=PRIORITY_CHOICES,
        default="Medium",
    )

    ticket_owner = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="tickets",
        blank=True
    )
    deal = models.ForeignKey(
    "deals.Deal",
    on_delete=models.PROTECT,
    related_name="tickets",
     )   
   
    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.ticket_name

