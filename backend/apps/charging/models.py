from django.db import models

from apps.common.constants.enums import PileStatus, PileType


class ChargingPile(models.Model):
    code = models.CharField(max_length=50, unique=True)
    location = models.CharField(max_length=200)
    lat = models.DecimalField(max_digits=10, decimal_places=7)
    lng = models.DecimalField(max_digits=10, decimal_places=7)
    type = models.CharField(max_length=10, choices=PileType.choices)
    power = models.DecimalField(max_digits=8, decimal_places=2)
    status = models.CharField(max_length=20, choices=PileStatus.choices, default=PileStatus.IDLE)
    price_per_kwh = models.DecimalField(max_digits=6, decimal_places=2)
    installed_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["code"]
