from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.messages import get_messages
from .models import User

class AccountsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.register_url = reverse('accounts:register')
        self.login_url = reverse('accounts:login')
        
    def test_register_success_message(self):
        """测试注册成功后是否只显示一条成功消息"""
        # 发送注册请求
        response = self.client.post(self.register_url, {
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'testpass123',
            'password2': 'testpass123',
            'phone': '13800138000'
        }, follow=True)
        
        # 检查是否重定向到登录页面
        self.assertRedirects(response, self.login_url)
        
        # 获取所有消息
        messages = list(get_messages(response.wsgi_request))
        
        # 检查是否只有一条消息
        self.assertEqual(len(messages), 1, f"期望1条消息，实际收到{len(messages)}条消息: {messages}")
        
        # 检查消息内容
        self.assertEqual(str(messages[0]), '注册成功，请登录')
        
    def test_register_duplicate_email(self):
        """测试邮箱已注册时是否显示正确的错误信息"""
        # 先创建一个用户
        User.objects.create_user(
            username='existinguser',
            email='existing@example.com',
            password='testpass123',
            phone='13800138000'
        )
        
        # 使用相同的邮箱注册
        response = self.client.post(self.register_url, {
            'username': 'newuser',
            'email': 'existing@example.com',
            'password1': 'testpass123',
            'password2': 'testpass123',
            'phone': '13800138001'
        })
        
        # 检查是否在注册页面
        self.assertTemplateUsed(response, 'accounts/register.html')
        
        # 检查表单错误
        self.assertFormError(response, 'form', 'email', '该邮箱已被注册')
        
        # 检查消息数量（应该没有消息，因为错误是通过表单显示的）
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 0, f"期望0条消息，实际收到{len(messages)}条消息: {messages}")
