from rest_framework.generics import ListAPIView
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from .models import OperationLog
from .serializers import OperationLogSerializer
from apps.users.permissions import IsAdmin


class OperationLogListView(ListAPIView):
    queryset = OperationLog.objects.select_related('user').all()
    serializer_class = OperationLogSerializer
    permission_classes = [IsAdmin]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['action']
    search_fields = ['user__username', 'target']
    ordering = ['-created_at']
