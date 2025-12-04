from django.db import models
from categories.models import Category

class Book(models.Model):
    STATUS = (('available', '可借'), ('borrowed', '已借完'))
    isbn = models.CharField('ISBN', max_length=20, unique=True, blank=True)
    title = models.CharField('书名', max_length=200, db_index=True)
    author = models.CharField('作者', max_length=100, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, verbose_name='分类')
    total = models.PositiveIntegerField('总册数', default=1)
    available = models.PositiveIntegerField('在馆册数', default=1)
    status = models.CharField('状态', max_length=10, choices=STATUS, default='available')
    created_at = models.DateTimeField('入库时间', auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'books'
        verbose_name = '图书'
        verbose_name_plural = '图书'