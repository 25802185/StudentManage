from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from .models import Course
from .serializers import CourseSerializer
from apps.users.permissions import IsAdminOrTeacher


class CourseViewSet(ModelViewSet):
    queryset = Course.objects.select_related('class_ref', 'teacher').all()
    serializer_class = CourseSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['class_ref']
    search_fields = ['name']
    permission_classes = [IsAdminOrTeacher]

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        if user.role == 'teacher' and hasattr(user, 'teacher_profile'):
            qs = qs.filter(class_ref=user.teacher_profile.class_ref)
        return qs
