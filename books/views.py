from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from accounts.decorators import admin_required
from .models import Book
from categories.models import Category

@login_required
def book_list(request):
    kw = request.GET.get('kw')
    category_id = request.GET.get('category')
    # 使用select_related优化外键查询性能，确保正确关联分类表
    qs = Book.objects.select_related('category').all()
    if kw:
        qs = qs.filter(title__icontains=kw)
    if category_id:
        qs = qs.filter(category_id=category_id)
    # 移除过于严格的过滤条件，确保所有有效图书都能显示
    # 只过滤掉完全没有标题的记录，但允许标题为空字符串
    qs = qs.exclude(title__isnull=True)
    paginator = Paginator(qs, 10)  # 每页 10 条
    page = request.GET.get('page')
    books = paginator.get_page(page)
    categories = Category.objects.all()
    return render(request, 'books/book_list.html', {'books': books, 'categories': categories, 'kw': kw})

import uuid

@admin_required
def book_add(request):
    # 获取所有分类
    categories = Category.objects.all()
    
    # 检查是否有分类数据，如果没有，提示用户
    if not categories.exists():
        messages.warning(request, '当前没有分类数据，请先添加分类')
        # 确保即使没有分类也能正确渲染页面
        return render(request, 'books/book_form.html', {'categories': categories})
        
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()  # 添加strip确保去除首尾空格
        author = request.POST.get('author', '').strip()
        category_id = request.POST.get('category')
        total = request.POST.get('total', '1')
        isbn = request.POST.get('isbn', '').strip()

        # 添加更多表单验证
        if not title:
            messages.error(request, '书名不能为空')
            return redirect('books:book_add')
        
        # 容错：分类必填
        if not category_id:
            messages.error(request, '必须选择分类')
            return redirect('books:book_add')
        
        # 验证总册数是否为有效数字
        try:
            total = int(total)
            if total <= 0:
                messages.error(request, '总册数必须大于0')
                return redirect('books:book_add')
        except ValueError:
            messages.error(request, '总册数必须是数字')
            return redirect('books:book_add')
        
        # 如果没有提供ISBN，则生成一个唯一的ISBN
        if not isbn:
            isbn = str(uuid.uuid4())[:13]  # 生成13位唯一标识符作为ISBN

        try:
            # 确保category_id是有效的分类ID
            category = Category.objects.get(id=category_id)
            
            # 创建图书记录
            Book.objects.create(
                title=title,
                author=author,
                category=category,  # 直接使用category对象而不是category_id
                isbn=isbn,
                total=total,
                available=total,
                status='available'  # 显式设置状态
            )
            messages.success(request, '图书已新增')
            return redirect('books:book_list')
        except Category.DoesNotExist:
            messages.error(request, '选择的分类不存在')
            return redirect('books:book_add')
        except IntegrityError:
            # 如果ISBN仍然重复，捕获异常并提供更具体的错误信息
            messages.error(request, '添加失败，ISBN已存在，请修改ISBN或不填写让系统自动生成')
            return redirect('books:book_add')
        except Exception as e:
            # 捕获其他所有异常，提供更详细的错误信息
            messages.error(request, f'添加失败: {str(e)}')
            return redirect('books:book_add')

    return render(request, 'books/book_form.html', {'categories': categories})

@admin_required
def book_edit(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book.title = request.POST['title']
        book.author = request.POST['author']
        book.category_id = request.POST['category']
        book.total = int(request.POST['total'])
        book.available = book.total  # 简单处理
        book.save()
        return redirect('books:book_list')
    categories = Category.objects.all()
    return render(request, 'books/book_form.html', {'book': book, 'categories': categories})

@admin_required
def book_delete(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book.delete()
        return redirect('books:book_list')
    return render(request, 'books/book_confirm_delete.html', {'book': book})