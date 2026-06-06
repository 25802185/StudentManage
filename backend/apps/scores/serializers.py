from rest_framework import serializers
from .models import Score


class ScoreSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.name', read_only=True)
    student_no = serializers.CharField(source='student.student_no', read_only=True)
    course_name = serializers.CharField(source='course.name', read_only=True)

    class Meta:
        model = Score
        fields = [
            'id', 'student', 'student_name', 'student_no',
            'course', 'course_name', 'score', 'semester',
            'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class ScoreBatchSerializer(serializers.Serializer):
    course = serializers.IntegerField()
    semester = serializers.CharField(max_length=20)
    scores = serializers.ListField(
        child=serializers.DictField(), help_text='[{"student": id, "score": float}, ...]'
    )
