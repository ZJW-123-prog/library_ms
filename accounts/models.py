from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    # 用户角色选项
    ROLE_CHOICES = (
        ('user', '普通用户'),
        ('admin', '管理员'),
    )
    
    phone = models.CharField('手机', max_length=20, blank=True)
    role = models.CharField('角色', max_length=10, choices=ROLE_CHOICES, default='user')
    created_at = models.DateTimeField('注册时间', auto_now_add=True)

    # 解决反向关联冲突
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name='accounts_user_groups',   # 别名
        related_query_name='user',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='accounts_user_permissions',  # 别名
        related_query_name='user',
    )

    class Meta:
        db_table = 'users'
        verbose_name = '用户'
        verbose_name_plural = '用户'