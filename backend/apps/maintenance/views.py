from rest_framework import decorators, response, viewsets

from apps.common.permissions import IsOperatorOrAdmin
from apps.maintenance.models import MaintenanceRecord
from apps.maintenance.serializers import MaintenanceRecordSerializer
from apps.maintenance.services import MaintenanceService


class MaintenanceRecordViewSet(viewsets.ModelViewSet):
    serializer_class = MaintenanceRecordSerializer
    permission_classes = [IsOperatorOrAdmin]
    queryset = MaintenanceRecord.objects.select_related("vehicle").all()

    def perform_create(self, serializer):
        MaintenanceService.create_record(serializer)

    @decorators.action(detail=True, methods=["patch"])
    def complete(self, request, pk=None):
        return response.Response(MaintenanceRecordSerializer(MaintenanceService.complete(self.get_object())).data)
