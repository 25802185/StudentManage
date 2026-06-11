from rest_framework import serializers
from .models import Course, Semester


class SemesterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Semester
        fields = ['id', 'name', 'is_current', 'created_at']
        read_only_fields = ['id', 'created_at']


class CourseSerializer(serializers.ModelSerializer):
    teacher_name = serializers.CharField(source='teacher.name', read_only=True, default='')
    class_name = serializers.CharField(source='class_ref.name', read_only=True, default='')
    semester_name = serializers.CharField(source='semester.name', read_only=True, default='')

    class Meta:
        model = Course
        fields = [
            'id', 'name', 'credit', 'class_ref', 'class_name',
            'teacher', 'teacher_name', 'semester', 'semester_name',
            'description', 'created_at',
        ]
        read_only_fields = ['id', 'created_at']
