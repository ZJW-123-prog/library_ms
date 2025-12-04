from django.urls import path
from . import views

app_name = 'admins'
urlpatterns = [
    path('', views.user_list, name='user_list'),
    path('edit/<int:user_id>/', views.user_edit, name='user_edit'),
    path('delete/<int:user_id>/', views.user_delete, name='user_delete'),
]