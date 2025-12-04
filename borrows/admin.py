from django.contrib import admin
from .models import BorrowRecord

@admin.register(BorrowRecord)
class BorrowRecordAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'book', 'borrow_date', 'due_date', 'status')
    list_filter = ('status',)
    search_fields = ('user__username', 'book__title')
    ordering = ('-id',)
    date_hierarchy = 'borrow_date'   # 顶部时间快速导航