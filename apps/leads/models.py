
from django.conf import settings
from django.db import models


class Lead(models.Model):

    STATUS_CHOICES = [
        ("New", "New"),
        ("Open", "Open"),
        ("In Progress", "In Progress"),
        ("Qualified", "Qualified"),
        ("Converted", "Converted"),
    ]


    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    country_code = models.CharField(max_length=10, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    job_title = models.CharField(max_length=150, blank=True)
    country=models.CharField(max_length=150,blank=True)
    
    contact_owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="owned_leads",
    )

    products = models.CharField(max_length=255, blank=True)
    company = models.CharField(max_length=150, blank=True)

    
    lead_status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="New",
    )


    city = models.CharField(max_length=100, blank=True)

    
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
