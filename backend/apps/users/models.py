from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Role(models.TextChoices):
        DRIVER = "DRIVER", "司机"
        OPERATOR = "OPERATOR", "运营"
        ADMIN = "ADMIN", "管理员"

    role = models.CharField(max_length=20, choices=Role.choices, default=Role.DRIVER)
    phone = models.CharField(max_length=30, blank=True)
