from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from accounts.decorators import admin_required
from .models import Category

@login_required
def category_list(request):
    categories = Category.objects.all()
    return render(request, 'categories/category_list.html', {'categories': categories})

@admin_required
def category_add(request):
    if request.method == 'POST':
        name = request.POST['name']
        description = request.POST['description']
        Category.objects.create(name=name, description=description)
        return redirect('categories:category_list')
    return render(request, 'categories/category_form.html')