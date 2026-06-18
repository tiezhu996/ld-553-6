from rest_framework import serializers

from apps.charging.models import ChargingPile


class ChargingPileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChargingPile
        fields = "__all__"
