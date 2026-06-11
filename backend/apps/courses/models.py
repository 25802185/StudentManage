from django.db import models
from apps.classes.models import ClassInfo
from apps.teachers.models import Teacher


class Semester(models.Model):
    name = models.CharField('学期名称', max_length=20, unique=True)
    is_current = models.BooleanField('当前学期', default=False)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        db_table = 'semesters'
        ordering = ['-name']
        verbose_name = '学期'
        verbose_name_plural = verbose_name

    def save(self, *args, **kwargs):
        if self.is_current:
            Semester.objects.filter(is_current=True).exclude(pk=self.pk).update(is_current=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Course(models.Model):
    name = models.CharField('课程名称', max_length=50)
    credit = models.FloatField('学分')
    class_ref = models.ForeignKey(
        ClassInfo, on_delete=models.CASCADE, related_name='courses', verbose_name='所属班级'
    )
    teacher = models.ForeignKey(
        Teacher, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='courses', verbose_name='授课教师'
    )
    semester = models.ForeignKey(Semester, on_delete=models.PROTECT, verbose_name='学期')
    description = models.TextField('课程描述', blank=True, default='')
    created_at = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        db_table = 'courses'
        verbose_name = '课程'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
