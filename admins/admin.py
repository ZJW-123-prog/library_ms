from django.contrib import admin
from .models import Admin

@admin.register(Admin)
class AdminAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'role', 'created_at')
    search_fields = ('username',)
    list_filter = ('role',)
    ordering = ('-id',)