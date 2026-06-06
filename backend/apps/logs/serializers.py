from rest_framework import serializers
from .models import OperationLog


class OperationLogSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True, default='')

    class Meta:
        model = OperationLog
        fields = ['id', 'user', 'username', 'action', 'target', 'detail', 'ip_address', 'created_at']
