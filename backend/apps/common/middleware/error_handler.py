import logging
from django.http import JsonResponse

from apps.common.exceptions import BusinessException, error_payload

logger = logging.getLogger(__name__)


class ErrorHandlerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            return self.get_response(request)
        except BusinessException as exc:
            return JsonResponse(error_payload(exc.status_code, exc.message, str(exc)), status=exc.status_code)
        except Exception as exc:
            logger.exception("Unhandled exception")
            return JsonResponse(error_payload(500, "服务器内部错误", str(exc)), status=500)
