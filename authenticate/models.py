from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    ROLE_CHOICES = (
    ('rider', 'Rider'),
    ('driver', 'Driver'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    current_latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    current_longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    ride_block_until = models.DateTimeField(null=True, blank=True)

    
