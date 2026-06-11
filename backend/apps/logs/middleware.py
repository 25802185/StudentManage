from .models import OperationLog

LOG_PATHS = [
    '/api/students/', '/api/teachers/', '/api/classes/',
    '/api/courses/', '/api/scores/',
]
LOG_METHODS = ['POST', 'PUT', 'DELETE', 'PATCH']

# 按长度倒序匹配，确保 /api/students/info-changes/ 先匹配到信息审核而非学生
PATH_MAP = [
    ('/api/students/info-changes/', '信息审核'),
    ('/api/students/', '学生'),
    ('/api/teachers/', '教师'),
    ('/api/classes/', '班级'),
    ('/api/courses/', '课程'),
    ('/api/scores/', '成绩'),
]

METHOD_MAP = {
    'POST': '新增',
    'PUT': '修改',
    'DELETE': '删除',
    'PATCH': '更新',
}


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
                method = request.method
                path = request.path
                action = METHOD_MAP.get(method, method)
                target = '未知'
                for p, name in PATH_MAP:
                    if p in path:
                        target = name
                        break
                detail = f'{action}{target}数据'
                if method == 'DELETE':
                    detail = f'删除了{target}记录'
                elif method == 'POST':
                    detail = f'新增了{target}数据'
                elif method in ('PUT', 'PATCH'):
                    detail = f'修改了{target}数据'

                OperationLog.objects.create(
                    user=request.user,
                    action=action,
                    target=target,
                    detail=detail,
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
