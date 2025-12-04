from django.urls import path
from . import views

app_name = 'categories'
urlpatterns = [
    path('', views.category_list, name='category_list'),
    path('add/', views.category_add, name='category_add'),
]