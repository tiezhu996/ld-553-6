from django.http import JsonResponse
from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

from apps.common.models import AuditLog
from apps.common.permissions import IsAdmin
from apps.common.serializers import AuditLogSerializer


@api_view(["GET"])
@permission_classes([AllowAny])
def health(request):
    return JsonResponse({"status": "ok"})


class AuditLogViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = AuditLogSerializer
    permission_classes = [IsAdmin]

    def get_queryset(self):
        queryset = AuditLog.objects.select_related("user").all()
        for field in ("entity_type", "entity_id"):
            value = self.request.query_params.get(field)
            if value:
                queryset = queryset.filter(**{field: value})
        if start := self.request.query_params.get("start_date"):
            queryset = queryset.filter(created_at__date__gte=start)
        if end := self.request.query_params.get("end_date"):
            queryset = queryset.filter(created_at__date__lte=end)
        return queryset
