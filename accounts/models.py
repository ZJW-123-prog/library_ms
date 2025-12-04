from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """用户模型类
    
    继承自Django的AbstractUser，扩展了自定义字段和功能
    支持普通用户和管理员两种角色
    """
    
    # 用户角色选项
    ROLE_CHOICES = (
        ('user', '普通用户'),   # 普通用户角色
        ('admin', '管理员'),     # 管理员角色
    )
    
    # 扩展用户信息字段
    phone = models.CharField('手机', max_length=20, blank=True, 
                           help_text='用户手机号码')
    role = models.CharField('角色', max_length=10, choices=ROLE_CHOICES, 
                          default='user', 
                          help_text='用户角色，默认为普通用户')
    created_at = models.DateTimeField('注册时间', auto_now_add=True, 
                                    help_text='用户注册时间')

    # 解决反向关联冲突
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name='accounts_user_groups',   # 别名，解决与auth.User的冲突
        related_query_name='user',
    )
    
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='accounts_user_permissions',  # 别名，解决与auth.User的冲突
        related_query_name='user',
    )

    def __str__(self):
        """模型对象的字符串表示
        
        返回用户名作为对象的字符串表示
        """
        return self.username

    class Meta:
        """模型元数据
        
        定义模型的数据库表名和显示名称
        """
        db_table = 'users'               # 数据库表名
        verbose_name = '用户'             # 模型单数显示名称
        verbose_name_plural = '用户'       # 模型复数显示名称