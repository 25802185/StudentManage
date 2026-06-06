from rest_framework.authentication import SessionAuthentication


class CsrfExemptSessionAuthentication(SessionAuthentication):
    """跳过 CSRF 验证的 Session 认证"""
    def enforce_csrf(self, request):
        return
