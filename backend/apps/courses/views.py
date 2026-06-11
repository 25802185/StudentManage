from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from .models import Course, Semester
from .serializers import CourseSerializer, SemesterSerializer
from apps.users.permissions import IsAdmin, IsAdminOrTeacher


class SemesterViewSet(ModelViewSet):
    queryset = Semester.objects.all()
    serializer_class = SemesterSerializer
    permission_classes = [IsAdmin]

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [IsAuthenticated()]
        return [IsAdmin()]

    @action(detail=True, methods=['put'])
    def set_current(self, request, pk=None):
        semester = self.get_object()
        semester.is_current = True
        semester.save()
        return Response({'message': f'已将 {semester.name} 设为当前学期'})


class CourseViewSet(ModelViewSet):
    queryset = Course.objects.select_related('class_ref', 'teacher', 'semester').all()
    serializer_class = CourseSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['class_ref', 'semester']
    search_fields = ['name']
    permission_classes = [IsAdminOrTeacher]

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        if user.role == 'teacher' and hasattr(user, 'teacher_profile'):
            class_ref = self.request.query_params.get('class_ref')
            if class_ref:
                qs = qs.filter(class_ref_id=class_ref)
            else:
                qs = qs.filter(class_ref=user.teacher_profile.class_ref)
        return qs
