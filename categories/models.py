from django.db import models


class Category(models.Model):
    """书籍分类模型类
    
    用于存储图书馆中的书籍分类信息，支持多层级分类结构
    """
    
    # 分类基本信息字段
    name = models.CharField('分类名称', max_length=50, unique=True, 
                          help_text='分类名称，必须唯一')
    description = models.TextField('描述', blank=True, 
                                 help_text='分类详细描述')
    
    # 时间戳字段
    created_at = models.DateTimeField('创建时间', auto_now_add=True, 
                                    help_text='分类创建时间')

    def __str__(self):
        """模型对象的字符串表示
        
        返回分类名称作为对象的字符串表示
        """
        return self.name

    class Meta:
        """模型元数据
        
        定义模型的数据库表名和显示名称
        """
        db_table = 'categories'               # 数据库表名
        verbose_name = '分类'                 # 模型单数显示名称
        verbose_name_plural = '分类'           # 模型复数显示名称