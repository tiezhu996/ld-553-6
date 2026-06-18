from apps.charging.models import ChargingPile
from apps.common.constants.enums import PileStatus
from apps.common.exceptions import BusinessException


class ChargingService:
    @staticmethod
    def set_status(pile: ChargingPile, status: str) -> ChargingPile:
        if status == PileStatus.FAULTY and pile.status not in {PileStatus.IDLE, PileStatus.CHARGING}:
            raise BusinessException("只有空闲或充电中的充电桩可以报故障")
        if status == PileStatus.IDLE and pile.status not in {PileStatus.FAULTY, PileStatus.MAINTENANCE}:
            raise BusinessException("只有故障或维护状态可以恢复为空闲")
        pile.status = status
        pile.save(update_fields=["status"])
        return pile

    @staticmethod
    def update_price(pile: ChargingPile, price) -> ChargingPile:
        pile.price_per_kwh = price
        pile.save(update_fields=["price_per_kwh"])
        return pile
