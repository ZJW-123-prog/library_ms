from django.contrib import admin
from .models import Book

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'category', 'total', 'available', 'status')
    list_filter = ('category', 'status')
    search_fields = ('title', 'author', 'isbn')
    ordering = ('-id',)