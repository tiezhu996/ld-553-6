import datetime as dt
import jwt
from django.conf import settings
from rest_framework import status, viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.common.permissions import IsAdmin
from apps.users.models import User
from apps.users.serializers import LoginSerializer, UserSerializer


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        payload = {
            "user_id": user.id,
            "role": user.role,
            "exp": dt.datetime.utcnow() + dt.timedelta(hours=8),
        }
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
        return Response({"access": token, "user": UserSerializer(user).data})


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [IsAdmin]
    queryset = User.objects.all()

    def create(self, request, *args, **kwargs):
        user = User.objects.create_user(
            username=request.data["username"],
            password=request.data.get("password", "TransitHub@123"),
            role=request.data.get("role", User.Role.DRIVER),
            email=request.data.get("email", ""),
        )
        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
