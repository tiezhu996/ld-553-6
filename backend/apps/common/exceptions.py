import logging
from django.conf import settings
from django.utils import timezone
from rest_framework.views import exception_handler

logger = logging.getLogger(__name__)


class BusinessException(Exception):
    status_code = 400

    def __init__(self, message: str, status_code: int | None = None):
        self.message = message
        if status_code:
            self.status_code = status_code
        super().__init__(message)


class ResourceNotFoundException(BusinessException):
    status_code = 404


class PermissionDeniedException(BusinessException):
    status_code = 403


def error_payload(code: int, message: str, detail: str = "") -> dict:
    payload = {"code": code, "message": message, "timestamp": timezone.now().isoformat()}
    if settings.DEBUG and detail:
        payload["detail"] = detail
    return payload


def drf_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response is None:
        return None
    message = response.data.get("detail", response.status_text) if isinstance(response.data, dict) else response.status_text
    response.data = error_payload(response.status_code, str(message), str(exc))
    logger.warning("DRF exception: %s", exc)
    return response
