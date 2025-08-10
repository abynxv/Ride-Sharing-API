from django.db import models
from authenticate.models import CustomUser


class Ride(models.Model):
    STATUS_CHOICES = [
        ("requested", "Requested"),
        ("matched", "Matched"),
        ("accepted", "Accepted"),
        ("in_progress", "In Progress"),
        ("completed", "Completed"),
    ]

    rider = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="rides")
    driver = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name="drives")

    ride_date = models.DateField(null=True, blank=True)
    pickup_location = models.CharField(max_length=255)
    pickup_latitude = models.FloatField()
    pickup_longitude = models.FloatField()

    dropoff_location = models.CharField(max_length=255)
    dropoff_latitude = models.FloatField()
    dropoff_longitude = models.FloatField()

    current_latitude = models.FloatField(null=True, blank=True)
    current_longitude = models.FloatField(null=True, blank=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="requested")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)