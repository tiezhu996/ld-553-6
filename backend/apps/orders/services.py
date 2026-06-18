from decimal import Decimal
from uuid import uuid4

from apps.common.constants.enums import OrderStatus, PaymentStatus
from apps.common.exceptions import BusinessException
from apps.orders.models import TripOrder


class OrderService:
    transitions = {
        OrderStatus.PENDING: {OrderStatus.ACCEPTED, OrderStatus.CANCELLED},
        OrderStatus.ACCEPTED: {OrderStatus.IN_PROGRESS},
        OrderStatus.IN_PROGRESS: {OrderStatus.COMPLETED},
    }

    @staticmethod
    def create_order(serializer, user) -> TripOrder:
        return serializer.save(user=user, order_no=f"TH{uuid4().hex[:12].upper()}", status=OrderStatus.PENDING)

    @classmethod
    def set_status(cls, order: TripOrder, status: str, vehicle_id=None) -> TripOrder:
        if status not in cls.transitions.get(order.status, set()):
            raise BusinessException("订单状态流转不合法")
        order.status = status
        if vehicle_id:
            order.vehicle_id = vehicle_id
        if status == OrderStatus.COMPLETED and not order.fare:
            order.fare = Decimal(order.distance) * Decimal("2.40")
        order.save()
        return order

    @staticmethod
    def pay(order: TripOrder) -> TripOrder:
        if order.payment_status != PaymentStatus.UNPAID:
            raise BusinessException("订单无需重复支付")
        order.payment_status = PaymentStatus.PAID
        order.save(update_fields=["payment_status", "updated_at"])
        return order
