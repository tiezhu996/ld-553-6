import jwt
from django.conf import settings
from rest_framework import authentication, exceptions

from apps.users.models import User


class JWTAuthentication(authentication.BaseAuthentication):
    keyword = "Bearer"

    def authenticate(self, request):
        header = authentication.get_authorization_header(request).decode()
        if not header:
            return None
        try:
            keyword, token = header.split(" ", 1)
        except ValueError:
            raise exceptions.AuthenticationFailed("认证头格式错误")
        if keyword != self.keyword:
            return None
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user = User.objects.get(id=payload["user_id"])
        except Exception as exc:
            raise exceptions.AuthenticationFailed("无效或过期的 token") from exc
        return user, token
