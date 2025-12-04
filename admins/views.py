from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from accounts.decorators import admin_required
from accounts.models import User

@admin_required
def user_list(request):
    # 获取搜索参数
    search_query = request.GET.get('search', '')
    
    # 基础查询集
    users = User.objects.all()
    
    # 如果有搜索查询，进行过滤
    if search_query:
        users = users.filter(
            username__icontains=search_query
        ) | users.filter(
            email__icontains=search_query
        ) | users.filter(
            phone__icontains=search_query
        )
    
    # 排序，最新创建的在前
    users = users.order_by('-created_at')
    
    # 分页，每页显示10条
    paginator = Paginator(users, 10)
    page = request.GET.get('page', 1)
    
    try:
        paginated_users = paginator.page(page)
    except PageNotAnInteger:
        paginated_users = paginator.page(1)
    except EmptyPage:
        paginated_users = paginator.page(paginator.num_pages)
    
    # 将角色映射为中文显示
    role_display = {'admin': '管理员', 'user': '普通用户'}
    
    return render(request, 'admins/user_list.html', {
        'users': paginated_users,
        'search_query': search_query,
        'role_display': role_display
    })

@admin_required
def user_edit(request, user_id):
    # 获取用户对象，如果不存在则返回404
    user = get_object_or_404(User, pk=user_id)
    
    # 角色选项
    ROLE_CHOICES = [
        ('user', '普通用户'),
        ('admin', '管理员')
    ]
    
    if request.method == 'POST':
        # 获取表单数据
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        role = request.POST.get('role')
        
        # 表单验证
        errors = []
        
        # 检查用户名是否已被其他用户使用
        existing_user = User.objects.filter(username=username).exclude(id=user_id).first()
        if existing_user:
            errors.append('用户名已存在')
        
        # 检查邮箱格式
        if email and not email.strip():
            errors.append('邮箱不能为空')
        
        if not username.strip():
            errors.append('用户名不能为空')
        
        if role not in ['user', 'admin']:
            errors.append('无效的角色选择')
        
        # 如果有错误，重新显示表单
        if errors:
            for error in errors:
                messages.error(request, error)
            return render(request, 'admins/user_edit.html', {
                'user': user,
                'ROLE_CHOICES': ROLE_CHOICES
            })
        
        # 更新用户信息
        user.username = username
        user.email = email
        user.phone = phone
        user.role = role
        user.save()
        
        messages.success(request, '用户信息更新成功')
        return redirect('admins:user_list')
    
    # GET请求，显示编辑表单
    return render(request, 'admins/user_edit.html', {
        'user': user,
        'ROLE_CHOICES': ROLE_CHOICES
    })

@admin_required
def user_delete(request, user_id):
    # 获取用户对象，如果不存在则返回404
    user = get_object_or_404(User, pk=user_id)
    
    # 防止删除当前登录的管理员自己
    if request.user.id == user.id:
        messages.error(request, '不能删除当前登录的用户自己')
        return redirect('admins:user_list')
    
    # 记录用户名用于显示消息
    username = user.username
    
    # 删除用户
    user.delete()
    
    messages.success(request, f'用户 "{username}" 已成功删除')
    return redirect('admins:user_list')
