from django.db import models

# Create your models here.
from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=150, unique=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(
    max_digits=10,
    decimal_places=2,
    default=0.00,
    )
   
    
    def __str__(self):
        return self.name

