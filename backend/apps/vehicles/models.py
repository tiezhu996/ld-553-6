from django.conf import settings
from django.db import models

from apps.common.constants.enums import VehicleStatus, VehicleType


class Vehicle(models.Model):
    plate_number = models.CharField(max_length=20, unique=True)
    type = models.CharField(max_length=20, choices=VehicleType.choices)
    brand = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    year = models.IntegerField()
    status = models.CharField(max_length=20, choices=VehicleStatus.choices, default=VehicleStatus.PENDING)
    driver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    insurance_expiry = models.DateField()
    lat = models.DecimalField(max_digits=10, decimal_places=7, default=31.2304000)
    lng = models.DecimalField(max_digits=10, decimal_places=7, default=121.4737000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
