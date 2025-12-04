#!/usr/bin/env python
"""
创建管理员用户的脚本
"""
import os
import sys
import django

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library_ms.settings')
django.setup()

from accounts.models import User

def create_admin():
    """创建一个管理员用户"""
    username = 'admin'
    email = 'admin@example.com'
    password = 'admin123'
    
    try:
        # 检查用户是否已存在
        user = User.objects.filter(username=username).first()
        if user:
            print(f'用户 {username} 已存在')
            # 如果存在，更新为管理员角色
            user.role = 'admin'
            user.save()
            print(f'已将 {username} 更新为管理员角色')
        else:
            # 创建新的管理员用户
            user = User.objects.create_superuser(
                username=username,
                email=email,
                password=password
            )
            user.role = 'admin'  # 设置为管理员角色
            user.save()
            print(f'管理员用户 {username} 创建成功')
            print(f'用户名: {username}')
            print(f'密码: {password}')
            print(f'邮箱: {email}')
    except Exception as e:
        print(f'创建管理员用户时出错: {e}')

if __name__ == '__main__':
    create_admin()