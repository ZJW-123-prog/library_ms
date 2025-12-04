from django.db import models
from books.models import Book
from accounts.models import User

class BorrowRecord(models.Model):
    STATUS = (("on", "在借"), ("off", "已还"), ("over", "逾期"))
    APPLY_STATUS = (("pending", "待审批"), ("approved", "已批准"), ("rejected", "已拒绝"))
    # 还书申请状态
    RETURN_REQUEST_STATUS = (("none", "无"), ("requested", "已申请"), ("confirmed", "已确认"))
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name='图书')
    borrow_date = models.DateField('借出日期', null=True, blank=True)
    due_date = models.DateField('应还日期', null=True, blank=True)
    return_date = models.DateField('实际归还', null=True, blank=True)
    status = models.CharField('状态', max_length=4, choices=STATUS, default='on')
    apply_status = models.CharField('申请状态', max_length=8, choices=APPLY_STATUS, default='pending')
    return_request_status = models.CharField('还书申请状态', max_length=10, choices=RETURN_REQUEST_STATUS, default='none')
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        db_table = 'borrow_records'
        verbose_name = '借阅记录'
        verbose_name_plural = '借阅记录'