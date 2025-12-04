from django.db import models
from categories.models import Category


class Book(models.Model):
    """书籍模型类
    
    用于存储图书馆中的书籍信息，包括基本信息、库存状态等
    """
    
    # 书籍状态常量定义
    STATUS = (
        ('available', '可借'),   # 书籍可借状态
        ('borrowed', '已借完'),   # 书籍已借完状态
    )
    
    # 书籍基本信息字段
    isbn = models.CharField('ISBN', max_length=20, unique=True, blank=True, 
                          help_text='国际标准书号，13位数字')
    title = models.CharField('书名', max_length=200, db_index=True, 
                           help_text='书籍标题，支持模糊查询')
    author = models.CharField('作者', max_length=100, blank=True, 
                            help_text='书籍作者')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, 
                               verbose_name='分类', 
                               help_text='书籍所属分类')
    
    # 库存信息字段
    total = models.PositiveIntegerField('总册数', default=1, 
                                     help_text='书籍总册数')
    available = models.PositiveIntegerField('在馆册数', default=1, 
                                         help_text='当前可借册数')
    status = models.CharField('状态', max_length=10, choices=STATUS, 
                            default='available', 
                            help_text='书籍当前状态')
    
    # 时间戳字段
    created_at = models.DateTimeField('入库时间', auto_now_add=True, 
                                    help_text='书籍添加到系统的时间')

    def __str__(self):
        """模型对象的字符串表示
        
        返回书籍标题作为对象的字符串表示
        """
        return self.title

    class Meta:
        """模型元数据
        
        定义模型的数据库表名和显示名称
        """
        db_table = 'books'               # 数据库表名
        verbose_name = '图书'             # 模型单数显示名称
        verbose_name_plural = '图书'       # 模型复数显示名称