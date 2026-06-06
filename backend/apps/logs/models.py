from django.db import models
from apps.users.models import User


class OperationLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='logs')
    action = models.CharField('操作类型', max_length=50)
    target = models.CharField('操作对象', max_length=100)
    detail = models.TextField('操作详情', blank=True, default='')
    ip_address = models.CharField('IP地址', max_length=50, blank=True, default='')
    created_at = models.DateTimeField('操作时间', auto_now_add=True)

    class Meta:
        db_table = 'operation_logs'
        verbose_name = '操作日志'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user} - {self.action} - {self.target}'
