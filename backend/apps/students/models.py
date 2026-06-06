from django.db import models
from apps.users.models import User
from apps.classes.models import ClassInfo


class Student(models.Model):
    GENDER_CHOICES = [('male', '男'), ('female', '女')]
    STATUS_CHOICES = [
        ('normal', '正常'),
        ('pending', '待审核'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    student_no = models.CharField('学号', max_length=20, unique=True)
    name = models.CharField('姓名', max_length=20)
    gender = models.CharField('性别', max_length=6, choices=GENDER_CHOICES)
    age = models.IntegerField('年龄', null=True, blank=True)
    class_ref = models.ForeignKey(
        ClassInfo, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='students', verbose_name='所属班级'
    )
    phone = models.CharField('联系电话', max_length=20, blank=True, default='')
    email = models.EmailField('邮箱', blank=True, default='')
    address = models.CharField('家庭地址', max_length=200, blank=True, default='')
    avatar = models.ImageField('头像', upload_to='avatars/', blank=True, null=True)
    status = models.CharField('状态', max_length=10, choices=STATUS_CHOICES, default='normal')

    class Meta:
        db_table = 'students'
        verbose_name = '学生'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f'{self.name} ({self.student_no})'


class InfoChangeRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', '待审核'),
        ('approved', '已通过'),
        ('rejected', '已驳回'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='change_requests')
    field_name = models.CharField('修改字段', max_length=50)
    old_value = models.CharField('原值', max_length=200)
    new_value = models.CharField('新值', max_length=200)
    status = models.CharField('状态', max_length=10, choices=STATUS_CHOICES, default='pending')
    reviewer = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='reviewed_changes', verbose_name='审核人'
    )
    review_time = models.DateTimeField('审核时间', null=True, blank=True)
    remark = models.CharField('审核备注', max_length=200, blank=True, default='')
    created_at = models.DateTimeField('申请时间', auto_now_add=True)

    class Meta:
        db_table = 'info_change_requests'
        verbose_name = '信息变更申请'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.student.name} - {self.field_name}'
