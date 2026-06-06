from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter
from .models import ClassInfo
from .serializers import ClassInfoSerializer
from apps.users.permissions import IsAdmin, IsAdminOrTeacher


class ClassInfoViewSet(ModelViewSet):
    queryset = ClassInfo.objects.all()
    serializer_class = ClassInfoSerializer
    filter_backends = [SearchFilter]
    search_fields = ['name', 'grade', 'major']

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [IsAdminOrTeacher()]
        return [IsAdmin()]
