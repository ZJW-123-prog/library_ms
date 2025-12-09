from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, label='邮箱', widget=forms.EmailInput(attrs={'class': 'form-control'}))
    phone = forms.CharField(required=False, label='手机', widget=forms.TextInput(attrs={'class': 'form-control'}))
    username = forms.CharField(required=True, label='用户名', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(required=True, label='密码', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(required=True, label='确认密码', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'phone')
        labels = {
            'username': '用户名',
            'email': '邮箱',
            'password1': '密码',
            'password2': '确认密码',
            'phone': '手机'
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('该邮箱已被注册')
        return email