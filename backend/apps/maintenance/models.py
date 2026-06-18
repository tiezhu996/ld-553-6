from django.db import models

from apps.vehicles.models import Vehicle


class MaintenanceRecord(models.Model):
    class Status(models.TextChoices):
        IN_PROGRESS = "IN_PROGRESS", "进行中"
        COMPLETED = "COMPLETED", "已完成"

    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name="maintenance_records")
    type = models.CharField(max_length=50)
    description = models.TextField()
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.IN_PROGRESS)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
