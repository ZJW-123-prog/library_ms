from django.urls import path
from . import views

app_name = 'borrows'
urlpatterns = [
    # 基础借阅记录
    path('', views.borrow_list, name='borrow_list'),
    path('add/', views.borrow_add, name='borrow_add'),
    path('<int:pk>/return/', views.borrow_return, name='borrow_return'),
    
    # 借阅申请相关
    path('book/<int:book_id>/request/', views.borrow_request, name='borrow_request'),
    path('approval/list/', views.borrow_approval_list, name='borrow_approval_list'),
    path('approval/<int:record_id>/<str:action>/', views.borrow_approve, name='borrow_approve'),
    
    # 还书申请相关
    path('<int:record_id>/return-request/', views.return_request, name='return_request'),
    path('return-request/list/', views.return_request_list, name='return_request_list'),
    path('return-request/<int:record_id>/confirm/', views.return_confirm, name='return_confirm'),
]