from django.db import models
from books.models import Book
from accounts.models import User


class BorrowRecord(models.Model):
    """借阅记录模型类
    
    用于存储用户的书籍借阅信息，包括借阅状态、申请状态、日期等
    """
    
    # 借阅状态常量
    STATUS = (
        ("on", "在借"),      # 书籍借阅中状态
        ("off", "已还"),     # 书籍已归还状态
        ("over", "逾期"),    # 书籍逾期未归还状态
    )
    
    # 借阅申请状态常量
    APPLY_STATUS = (
        ("pending", "待审批"),   # 借阅申请待审批状态
        ("approved", "已批准"),  # 借阅申请已批准状态
        ("rejected", "已拒绝"),  # 借阅申请已拒绝状态
    )
    
    # 还书申请状态常量
    RETURN_REQUEST_STATUS = (
        ("none", "无"),         # 无还书申请状态
        ("requested", "已申请"),  # 已提交还书申请状态
        ("confirmed", "已确认"),  # 还书申请已确认状态
    )
    
    # 关联字段
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户', 
                           help_text='借阅书籍的用户')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name='图书', 
                           help_text='被借阅的书籍')
    
    # 日期字段
    borrow_date = models.DateField('借出日期', null=True, blank=True, 
                                 help_text='书籍实际借出日期')
    due_date = models.DateField('应还日期', null=True, blank=True, 
                               help_text='书籍应归还日期')
    return_date = models.DateField('实际归还', null=True, blank=True, 
                                 help_text='书籍实际归还日期')
    
    # 状态字段
    status = models.CharField('状态', max_length=4, choices=STATUS, default='on', 
                            help_text='借阅记录状态')
    apply_status = models.CharField('申请状态', max_length=8, choices=APPLY_STATUS, 
                                  default='pending', 
                                  help_text='借阅申请状态')
    return_request_status = models.CharField('还书申请状态', max_length=10, 
                                           choices=RETURN_REQUEST_STATUS, 
                                           default='none', 
                                           help_text='还书申请状态')
    
    # 时间戳字段
    created_at = models.DateTimeField('创建时间', auto_now_add=True, 
                                    help_text='借阅记录创建时间')
    updated_at = models.DateTimeField('更新时间', auto_now=True, 
                                    help_text='借阅记录最后更新时间')

    def __str__(self):
        """模型对象的字符串表示
        
        返回用户借阅书籍的简要信息
        """
        return f"{self.user.username} - {self.book.title}"

    class Meta:
        """模型元数据
        
        定义模型的数据库表名和显示名称
        """
        db_table = 'borrow_records'           # 数据库表名
        verbose_name = '借阅记录'             # 模型单数显示名称
        verbose_name_plural = '借阅记录'       # 模型复数显示名称