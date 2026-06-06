from django.db import models


class ClassInfo(models.Model):
    name = models.CharField('班级名称', max_length=50)
    grade = models.CharField('年级', max_length=20)
    major = models.CharField('专业', max_length=50)
    student_count = models.IntegerField('学生人数', default=0)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        db_table = 'classes'
        verbose_name = '班级'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']

    def __str__(self):
        return self.name
