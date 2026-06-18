from rest_framework import serializers

from apps.common.models import AuditLog


class AuditLogSerializer(serializers.ModelSerializer):
    operator = serializers.CharField(source="user.username", read_only=True)

    class Meta:
        model = AuditLog
        fields = "__all__"


class CommonResponseSerializer(serializers.Serializer):
    code = serializers.IntegerField()
    message = serializers.CharField()
    data = serializers.JSONField(required=False)
