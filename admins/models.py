from django.db import models

class Admin(models.Model):
    ROLE = (('super', '超级管理员'), ('normal', '普通管理员'))
    username = models.CharField('账号', max_length=30, unique=True)
    password = models.CharField('密码', max_length=128)
    role = models.CharField('角色', max_length=10, choices=ROLE, default='normal')
    created_at = models.DateTimeField('创建时间', auto_now_add=True)

    def __str__(self):
        return self.username

    class Meta:
        db_table = 'admins'
        verbose_name = '管理员'
        verbose_name_plural = '管理员'