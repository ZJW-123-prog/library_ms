from django.db import models


class Admin(models.Model):
    """管理员模型类
    
    用于管理系统管理员账号，支持超级管理员和普通管理员两种角色
    """
    
    # 管理员角色常量
    ROLE = (
        ('super', '超级管理员'),  # 拥有系统最高权限
        ('normal', '普通管理员'), # 拥有普通管理权限
    )
    
    # 字段定义
    username = models.CharField('账号', max_length=30, unique=True, 
                               help_text='管理员登录账号，必须唯一')
    password = models.CharField('密码', max_length=128, 
                              help_text='管理员登录密码，加密存储')
    role = models.CharField('角色', max_length=10, choices=ROLE, default='normal', 
                          help_text='管理员角色，默认普通管理员')
    created_at = models.DateTimeField('创建时间', auto_now_add=True, 
                                    help_text='管理员账号创建时间')

    def __str__(self):
        """模型对象的字符串表示
        
        返回管理员的用户名
        """
        return self.username

    class Meta:
        """模型元数据
        
        定义模型的数据库表名和显示名称
        """
        db_table = 'admins'                 # 数据库表名
        verbose_name = '管理员'               # 模型单数显示名称
        verbose_name_plural = '管理员'         # 模型复数显示名称