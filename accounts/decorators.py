from django.http import HttpResponseForbidden
from django.shortcuts import render


def admin_required(view_func):
    """
    自定义装饰器，确保只有管理员角色的用户才能访问
    """
    def _wrapped_view(request, *args, **kwargs):
        # 检查用户是否已登录且角色为管理员
        if request.user.is_authenticated and request.user.role == 'admin':
            return view_func(request, *args, **kwargs)
        else:
            # 非管理员用户访问时，返回403禁止访问页面
            return render(request, 'accounts/403.html', status=403)
    return _wrapped_view