from django.db import models
from apps.users.models import User
from apps.classes.models import ClassInfo


class Teacher(models.Model):
    GENDER_CHOICES = [('male', '男'), ('female', '女')]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='teacher_profile')
    teacher_no = models.CharField('工号', max_length=20, unique=True)
    name = models.CharField('姓名', max_length=20)
    gender = models.CharField('性别', max_length=6, choices=GENDER_CHOICES)
    title = models.CharField('职称', max_length=20, blank=True, default='')
    phone = models.CharField('联系电话', max_length=20, blank=True, default='')
    email = models.EmailField('邮箱', blank=True, default='')
    class_ref = models.ForeignKey(
        ClassInfo, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='teachers', verbose_name='所带班级'
    )

    class Meta:
        db_table = 'teachers'
        verbose_name = '教师'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f'{self.name} ({self.teacher_no})'
