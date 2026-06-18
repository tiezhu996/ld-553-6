import json

from apps.common.models import AuditLog


class AuditLogMiddleware:
    WATCH_PREFIXES = ("/api/vehicles", "/api/charging-piles", "/api/orders", "/api/maintenance-records")
    WRITE_METHODS = {"POST", "PUT", "PATCH", "DELETE"}

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        body_summary = self._summary(request)
        response = self.get_response(request)
        if request.method in self.WRITE_METHODS and request.path.startswith(self.WATCH_PREFIXES):
            AuditLog.objects.create(
                user=request.user if getattr(request, "user", None) and request.user.is_authenticated else None,
                method=request.method,
                path=request.path,
                request_body=body_summary,
                response_status=response.status_code,
                ip_address=self._ip(request),
                user_agent=request.META.get("HTTP_USER_AGENT", "")[:300],
                entity_type=self._entity_type(request.path),
                entity_id=self._entity_id(request.path),
            )
        return response

    def _summary(self, request) -> str:
        try:
            payload = json.loads(request.body.decode() or "{}")
            for key in ("password", "token", "access"):
                if key in payload:
                    payload[key] = "***"
            return json.dumps(payload, ensure_ascii=False)[:1000]
        except Exception:
            return ""

    def _ip(self, request) -> str | None:
        forwarded = request.META.get("HTTP_X_FORWARDED_FOR")
        return (forwarded.split(",")[0] if forwarded else request.META.get("REMOTE_ADDR")) or None

    def _entity_type(self, path: str) -> str:
        parts = [p for p in path.split("/") if p]
        return parts[1] if len(parts) > 1 else ""

    def _entity_id(self, path: str) -> str:
        parts = [p for p in path.split("/") if p]
        for part in parts[2:]:
            if part.isdigit():
                return part
        return ""
