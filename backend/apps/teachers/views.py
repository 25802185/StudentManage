from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status as http_status
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from .models import Teacher
from .serializers import TeacherSerializer, TeacherCreateSerializer
from apps.users.permissions import IsAdmin, IsAdminOrTeacher


class TeacherViewSet(ModelViewSet):
    queryset = Teacher.objects.select_related('user', 'class_ref').all()
    filter_backends = [SearchFilter]
    search_fields = ['name', 'teacher_no']

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [IsAdminOrTeacher()]
        if self.action in ['update', 'partial_update']:
            return [IsAuthenticated()]
        return [IsAdmin()]

    def get_serializer_class(self):
        if self.action == 'create':
            return TeacherCreateSerializer
        return TeacherSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        teacher = serializer.save()
        return Response({
            'detail': '新增成功',
            'password': teacher._generated_password,
            'username': teacher.teacher_no,
        }, status=http_status.HTTP_201_CREATED)

    @action(detail=True, methods=['put'], url_path='toggle')
    def toggle_active(self, request, pk=None):
        teacher = self.get_object()
        teacher.user.is_active = not teacher.user.is_active
        teacher.user.save()
        return Response({'is_active': teacher.user.is_active})
