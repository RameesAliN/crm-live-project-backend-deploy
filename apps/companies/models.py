from django.conf import settings
from django.db import models


class Company(models.Model):

    TYPE_CHOICES = [
        ("Customer", "Customer"),
        ("Prospect", "Prospect"),
        ("Partner", "Partner"),
        ("Other", "Other"),
    ]

    domain = models.CharField(max_length=255, blank=True)
    company_name = models.CharField(max_length=150)

    company_owner = models.ManyToManyField(
    settings.AUTH_USER_MODEL,
    blank=True,
    related_name="owned_companies",)

    industry = models.CharField(max_length=150, blank=True)
    type = models.CharField(max_length=50,choices=TYPE_CHOICES,blank=True,)
    city = models.CharField(max_length=100)
    country_region = models.CharField(max_length=100)
    no_of_employees = models.PositiveIntegerField()
    annual_revenue = models.DecimalField(max_digits=15,decimal_places=2,)
    country_code = models.CharField(max_length=10, blank=True)
    phone_number = models.CharField(max_length=20)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.company_name