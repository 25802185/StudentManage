from rest_framework import serializers
from .models import Student, InfoChangeRequest
from apps.users.models import User


class StudentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    class_name = serializers.CharField(source='class_ref.name', read_only=True, default='')

    class Meta:
        model = Student
        fields = [
            'id', 'user', 'username', 'student_no', 'name', 'gender', 'age',
            'class_ref', 'class_name', 'phone', 'email', 'address', 'avatar', 'status',
        ]
        read_only_fields = ['id', 'status']


class StudentCreateSerializer(serializers.Serializer):
    student_no = serializers.CharField(max_length=20)
    name = serializers.CharField(max_length=20)
    gender = serializers.ChoiceField(choices=[('male', '男'), ('female', '女')])
    age = serializers.IntegerField(required=False, allow_null=True)
    class_ref_id = serializers.IntegerField(required=False, allow_null=True)
    phone = serializers.CharField(max_length=20, required=False, default='')
    email = serializers.EmailField(required=False, default='')
    address = serializers.CharField(max_length=200, required=False, default='')

    def validate_student_no(self, value):
        if Student.objects.filter(student_no=value).exists():
            raise serializers.ValidationError('学号已存在')
        return value

    def create(self, validated_data):
        from apps.classes.models import ClassInfo
        class_ref_id = validated_data.pop('class_ref_id', None)
        class_ref = ClassInfo.objects.filter(id=class_ref_id).first() if class_ref_id else None
        username = validated_data['student_no']
        password = username[-6:]
        user = User.objects.create_user(
            username=username, password=password, role='student', is_active=True,
        )
        student = Student.objects.create(user=user, class_ref=class_ref, **validated_data)
        if class_ref:
            class_ref.student_count = class_ref.students.count()
            class_ref.save()
        return student


class StudentUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['name', 'gender', 'age', 'class_ref', 'phone', 'email', 'address']


class InfoChangeRequestSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.name', read_only=True)

    class Meta:
        model = InfoChangeRequest
        fields = [
            'id', 'student', 'student_name', 'field_name', 'old_value',
            'new_value', 'status', 'reviewer', 'review_time', 'remark', 'created_at',
        ]
        read_only_fields = ['id', 'status', 'reviewer', 'review_time', 'created_at']
