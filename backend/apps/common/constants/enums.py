from django.db import models


class VehicleStatus(models.TextChoices):
    OPERATING = "OPERATING", "运营中"
    MAINTENANCE = "MAINTENANCE", "维修中"
    DISABLED = "DISABLED", "停用/报废"
    PENDING = "PENDING", "待审核"


class VehicleType(models.TextChoices):
    BUS = "BUS", "公交"
    TAXI = "TAXI", "出租"
    RIDE_HAILING = "RIDE_HAILING", "网约车"
    LOGISTICS = "LOGISTICS", "物流"


class PileType(models.TextChoices):
    FAST = "FAST", "快充"
    SLOW = "SLOW", "慢充"


class PileStatus(models.TextChoices):
    IDLE = "IDLE", "空闲"
    CHARGING = "CHARGING", "充电中"
    FAULTY = "FAULTY", "故障"
    MAINTENANCE = "MAINTENANCE", "维护"


class OrderStatus(models.TextChoices):
    PENDING = "PENDING", "待接单"
    ACCEPTED = "ACCEPTED", "已接单"
    IN_PROGRESS = "IN_PROGRESS", "进行中"
    COMPLETED = "COMPLETED", "已完成"
    CANCELLED = "CANCELLED", "已取消"


class PaymentStatus(models.TextChoices):
    UNPAID = "UNPAID", "未支付"
    PAID = "PAID", "已支付"
    REFUNDED = "REFUNDED", "已退款"
