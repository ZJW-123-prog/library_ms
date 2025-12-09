from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.contrib.auth.decorators import login_required

# 创建一个视图，根据用户是否登录重定向到不同页面
class HomeRedirectView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            # 已登录用户跳转到图书列表
            return '/books/'
        else:
            # 未登录用户跳转到登录页面
            return '/login/'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomeRedirectView.as_view()),  # 根据登录状态重定向
    path('books/', include('books.urls')),
    path('borrows/', include('borrows.urls')),
    path('categories/', include('categories.urls')),
    path('admins/', include('admins.urls')),
    # 添加重定向解决accounts/login/路径问题
    path('accounts/login/', RedirectView.as_view(url='/login/')),
    path('accounts/logout/', RedirectView.as_view(url='/logout/')),
    path('', include('accounts.urls')),
]