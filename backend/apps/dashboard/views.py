from rest_framework.decorators import api_view
from rest_framework.response import Response

from apps.dashboard.services import DashboardService


@api_view(["GET"])
def overview(request):
    return Response(DashboardService.overview())


@api_view(["GET"])
def order_trend(request):
    return Response(DashboardService.order_trend())


@api_view(["GET"])
def revenue_stats(request):
    return Response(DashboardService.revenue_stats())
