from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class MyUserAdmin(UserAdmin):
    list_display = ('id', 'username', 'email', 'phone', 'date_joined', 'is_active')
    search_fields = ('username', 'email', 'phone')
    list_filter = ('is_active', 'date_joined')
    ordering = ('-id',)