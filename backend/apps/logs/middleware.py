from .models import OperationLog

LOG_PATHS = [
    '/api/students/', '/api/teachers/', '/api/classes/',
    '/api/courses/', '/api/scores/', '/api/info-changes/',
]
LOG_METHODS = ['POST', 'PUT', 'DELETE', 'PATCH']


class OperationLogMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if (
            request.method in LOG_METHODS
            and any(path in request.path for path in LOG_PATHS)
            and request.user.is_authenticated
        ):
            try:
                OperationLog.objects.create(
                    user=request.user,
                    action=request.method,
                    target=request.path,
                    detail=f'{request.method} {request.path}',
                    ip_address=self.get_client_ip(request),
                )
            except Exception:
                pass
        return response

    def get_client_ip(self, request):
        x_forwarded = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded:
            return x_forwarded.split(',')[0]
        return request.META.get('REMOTE_ADDR', '')
