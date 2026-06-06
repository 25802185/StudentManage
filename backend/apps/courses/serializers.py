from rest_framework import serializers
from .models import Course


class CourseSerializer(serializers.ModelSerializer):
    teacher_name = serializers.CharField(source='teacher.name', read_only=True, default='')
    class_name = serializers.CharField(source='class_ref.name', read_only=True, default='')

    class Meta:
        model = Course
        fields = [
            'id', 'name', 'credit', 'class_ref', 'class_name',
            'teacher', 'teacher_name', 'description', 'created_at',
        ]
        read_only_fields = ['id', 'created_at']
