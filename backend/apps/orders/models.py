from django.conf import settings
from django.db import models

from apps.common.constants.enums import OrderStatus, PaymentStatus
from apps.vehicles.models import Vehicle


class TripOrder(models.Model):
    order_no = models.CharField(max_length=50, unique=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.SET_NULL, null=True, blank=True)
    start_location = models.CharField(max_length=200)
    end_location = models.CharField(max_length=200)
    start_lat = models.DecimalField(max_digits=10, decimal_places=7)
    start_lng = models.DecimalField(max_digits=10, decimal_places=7)
    end_lat = models.DecimalField(max_digits=10, decimal_places=7)
    end_lng = models.DecimalField(max_digits=10, decimal_places=7)
    distance = models.DecimalField(max_digits=10, decimal_places=2)
    duration = models.IntegerField()
    fare = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=OrderStatus.choices, default=OrderStatus.PENDING)
    payment_status = models.CharField(max_length=20, choices=PaymentStatus.choices, default=PaymentStatus.UNPAID)
    rating = models.IntegerField(null=True, blank=True)
    comment = models.CharField(max_length=500, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
