from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import UserRegisterForm

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '注册成功，请登录')
            return redirect('accounts:login')
    else:
        form = UserRegisterForm()
    return render(request, 'accounts/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is None and '@' in username:
            try:
                from .models import User
                real_user = User.objects.get(email=username)
                user = authenticate(request, username=real_user.username, password=password)
            except User.DoesNotExist:
                pass
        if user:
            login(request, user)
            # 根据用户角色跳转到不同页面
            if user.role == 'admin':
                return redirect('books:book_list')  # 管理员跳转到图书列表
            else:
                return redirect('borrows:borrow_list')  # 普通用户跳转到借阅记录
        else:
            # 清除现有的消息，避免重复显示
            storage = messages.get_messages(request)
            storage.used = True  # 标记消息已被使用
            messages.error(request, '用户名/密码错误')
    return render(request, 'accounts/login.html')

@login_required
def profile(request):
    return render(request, 'accounts/profile.html')

@login_required
def user_logout(request):
    logout(request)
    messages.info(request, '已退出登录')
    return redirect('accounts:login')