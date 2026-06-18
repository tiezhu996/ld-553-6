from django.urls import path
from apps.users.views import LoginView

urlpatterns = [path("login/", LoginView.as_view())]
