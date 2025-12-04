from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url='/login/')),  # 首页跳转到登录页面
    path('books/', include('books.urls')),
    path('borrows/', include('borrows.urls')),
    path('categories/', include('categories.urls')),
    path('admins/', include('admins.urls')),
    # 添加重定向解决accounts/login/路径问题
    path('accounts/login/', RedirectView.as_view(url='/login/')),
    path('accounts/logout/', RedirectView.as_view(url='/logout/')),
    path('', include('accounts.urls')),
]