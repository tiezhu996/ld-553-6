from django.urls import path

from apps.dashboard import views

urlpatterns = [
    path("overview/", views.overview),
    path("order-trend/", views.order_trend),
    path("revenue-stats/", views.revenue_stats),
]
