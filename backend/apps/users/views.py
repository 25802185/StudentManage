from django.contrib.auth import authenticate, login, logout
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import LoginSerializer, UserSerializer, ChangePasswordSerializer


class LoginView(APIView):
    permission_classes = []

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(
            request,
            username=serializer.validated_data['username'],
            password=serializer.validated_data['password'],
        )
        if user is None:
            return Response({'detail': '用户名或密码错误'}, status=status.HTTP_401_UNAUTHORIZED)
        if not user.is_active:
            return Response({'detail': '账号已被禁用'}, status=status.HTTP_403_FORBIDDEN)
        login(request, user)
        return Response(UserSerializer(user).data)


class LogoutView(APIView):
    def post(self, request):
        logout(request)
        return Response({'detail': '已退出登录'})


class UserInfoView(APIView):
    def get(self, request):
        user = request.user
        data = UserSerializer(user).data
        if user.role == 'student' and hasattr(user, 'student_profile'):
            data['name'] = user.student_profile.name
            data['student_no'] = user.student_profile.student_no
        elif user.role == 'teacher' and hasattr(user, 'teacher_profile'):
            data['name'] = user.teacher_profile.name
            data['teacher_no'] = user.teacher_profile.teacher_no
        return Response(data)


class ChangePasswordView(APIView):
    def put(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = request.user
        if not user.check_password(serializer.validated_data['old_password']):
            return Response({'detail': '旧密码错误'}, status=status.HTTP_400_BAD_REQUEST)
        user.set_password(serializer.validated_data['new_password'])
        user.save()
        login(request, user)
        return Response({'detail': '密码修改成功'})
