from rest_framework import serializers
from .models import Teacher
from apps.users.models import User


class TeacherSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    class_name = serializers.CharField(source='class_ref.name', read_only=True, default='')
    is_active = serializers.BooleanField(source='user.is_active', read_only=True)

    class Meta:
        model = Teacher
        fields = [
            'id', 'user', 'username', 'teacher_no', 'name', 'gender',
            'title', 'phone', 'email', 'class_ref', 'class_name', 'is_active',
        ]
        read_only_fields = ['id', 'user', 'username', 'teacher_no', 'name', 'gender', 'class_ref', 'class_name', 'is_active']


class TeacherCreateSerializer(serializers.Serializer):
    teacher_no = serializers.CharField(max_length=20)
    name = serializers.CharField(max_length=20)
    gender = serializers.ChoiceField(choices=[('male', '男'), ('female', '女')])
    title = serializers.CharField(max_length=20, required=False, default='')
    phone = serializers.CharField(max_length=20, required=False, default='')
    email = serializers.EmailField(required=False, default='')
    class_ref = serializers.IntegerField(required=False, allow_null=True)
    password = serializers.CharField(max_length=128, required=False, write_only=True)

    def validate_teacher_no(self, value):
        if Teacher.objects.filter(teacher_no=value).exists():
            raise serializers.ValidationError('工号已存在')
        return value

    def create(self, validated_data):
        from apps.classes.models import ClassInfo
        class_ref_id = validated_data.pop('class_ref', None)
        custom_password = validated_data.pop('password', None)
        class_ref = ClassInfo.objects.filter(id=class_ref_id).first() if class_ref_id else None
        username = validated_data['teacher_no']
        password = custom_password if custom_password else username[-6:]
        user = User.objects.create_user(
            username=username, password=password, role='teacher', is_active=True,
        )
        teacher = Teacher.objects.create(user=user, class_ref=class_ref, **validated_data)
        teacher._generated_password = password
        return teacher
