from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', '管理员'),
        ('teacher', '教师'),
        ('student', '学生'),
    ]
    role = models.CharField('角色', max_length=10, choices=ROLE_CHOICES, default='student')
    created_at = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        db_table = 'users'
        verbose_name = '用户'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f'{self.username} ({self.get_role_display()})'
