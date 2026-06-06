from django.db import models
from apps.students.models import Student
from apps.courses.models import Course


class Score(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='scores')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='scores')
    score = models.FloatField('成绩')
    semester = models.CharField('学期', max_length=20)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        db_table = 'scores'
        verbose_name = '成绩'
        verbose_name_plural = verbose_name
        unique_together = ['student', 'course', 'semester']

    def __str__(self):
        return f'{self.student.name} - {self.course.name}: {self.score}'
