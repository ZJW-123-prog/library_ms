#!/usr/bin/env python3
"""
测试注册功能的消息显示是否正常
"""

from django.test import Client, RequestFactory
from django.urls import reverse
from django.contrib.messages import get_messages
import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library_ms.settings')

import django
django.setup()

from accounts.views import register
from accounts.forms import UserRegisterForm

def test_register_success_message():
    """测试注册成功后是否只显示一条成功消息"""
    client = Client()
    register_url = reverse('accounts:register')
    login_url = reverse('accounts:login')
    
    # 发送注册请求
    response = client.post(register_url, {
        'username': 'testuser123',
        'email': 'test123@example.com',
        'password1': 'testpass123',
        'password2': 'testpass123',
        'phone': '13800138000'
    }, follow=True)
    
    # 检查是否重定向到登录页面
    assert response.status_code == 200
    assert login_url in response.redirect_chain[-1][0]
    
    # 获取所有消息
    messages = list(get_messages(response.wsgi_request))
    
    # 检查是否只有一条消息
    assert len(messages) == 1, f"期望1条消息，实际收到{len(messages)}条消息: {messages}"
    
    # 检查消息内容
    assert str(messages[0]) == '注册成功，请登录'
    
    print("✓ 注册成功消息测试通过！")

def test_register_form_errors():
    """测试注册表单错误时是否正确显示错误信息"""
    client = Client()
    register_url = reverse('accounts:register')
    
    # 使用相同的用户名注册两次
    # 第一次注册
    client.post(register_url, {
        'username': 'duplicateuser',
        'email': 'duplicate@example.com',
        'password1': 'testpass123',
        'password2': 'testpass123',
        'phone': '13800138000'
    }, follow=True)
    
    # 第二次使用相同的用户名注册
    response = client.post(register_url, {
        'username': 'duplicateuser',
        'email': 'another@example.com',
        'password1': 'testpass123',
        'password2': 'testpass123',
        'phone': '13800138001'
    })
    
    # 检查是否返回表单错误
    assert response.status_code == 200
    assert 'form' in response.context
    form = response.context['form']
    assert form.errors
    assert 'username' in form.errors
    
    # 检查消息数量（应该没有消息，因为错误是通过表单显示的）
    messages = list(get_messages(response.wsgi_request))
    assert len(messages) == 0, f"期望0条消息，实际收到{len(messages)}条消息: {messages}"
    
    print("✓ 注册表单错误测试通过！")

if __name__ == '__main__':
    print("开始测试注册功能的消息显示...")
    
    try:
        test_register_success_message()
        test_register_form_errors()
        print("\n✅ 所有测试通过！注册功能的消息显示正常。")
        sys.exit(0)
    except AssertionError as e:
        print(f"\n❌ 测试失败: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ 测试出现异常: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
