from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from accounts.decorators import admin_required
from .models import BorrowRecord
from books.models import Book
from accounts.models import User
from django.utils import timezone
from datetime import timedelta

@login_required
def borrow_list(request):
    # 普通用户只能查看自己的借阅记录，管理员可以查看所有记录
    if request.user.role == 'admin':
        records = BorrowRecord.objects.select_related('user', 'book').all()
    else:
        records = BorrowRecord.objects.select_related('user', 'book').filter(user=request.user)
    return render(request, 'borrows/borrow_list.html', {'records': records})

@login_required
def borrow_request(request, book_id):
    # 普通用户提交借阅申请
    if request.user.role == 'admin':
        messages.error(request, '管理员不能提交借阅申请')
        return redirect('books:book_list')
    
    # 获取图书并检查是否有库存
    book = get_object_or_404(Book, pk=book_id)
    if book.available <= 0:
        messages.error(request, '该图书暂时没有可借库存')
        return redirect('books:book_list')
    
    # 检查用户是否已经有该图书的待审批申请
    existing_request = BorrowRecord.objects.filter(
        user=request.user,
        book=book,
        apply_status='pending'
    ).exists()
    
    if existing_request:
        messages.warning(request, '您已经提交了该图书的借阅申请，请等待审批')
        return redirect('books:book_list')
    
    # 创建借阅申请记录
    BorrowRecord.objects.create(
        user=request.user,
        book=book,
        apply_status='pending'
    )
    
    messages.success(request, '借阅申请已提交，请等待管理员审批')
    return redirect('books:book_list')

@login_required
def return_request(request, record_id):
    # 普通用户提交还书申请
    if request.user.role == 'admin':
        messages.error(request, '管理员不能提交还书申请')
        return redirect('borrows:borrow_list')
    
    # 获取借阅记录并验证所有权
    record = get_object_or_404(BorrowRecord, pk=record_id, user=request.user)
    
    # 检查记录状态
    if record.status != 'on':
        messages.error(request, '该借阅记录当前不能申请还书')
        return redirect('borrows:borrow_list')
    
    # 检查是否已经提交还书申请
    if record.return_request_status == 'requested':
        messages.warning(request, '您已经提交了还书申请，请等待管理员确认')
        return redirect('borrows:borrow_list')
    
    # 更新还书申请状态
    record.return_request_status = 'requested'
    record.save()
    
    messages.success(request, '还书申请已提交，请等待管理员确认')
    return redirect('borrows:borrow_list')

@admin_required
def borrow_approval_list(request):
    # 管理员查看待审批的借阅申请
    pending_records = BorrowRecord.objects.select_related('user', 'book').filter(apply_status='pending')
    return render(request, 'borrows/borrow_approval_list.html', {'pending_records': pending_records})

@admin_required
def borrow_approve(request, record_id, action):
    # 处理借阅申请的审批
    record = get_object_or_404(BorrowRecord, pk=record_id, apply_status='pending')
    
    if request.method == 'POST':
        if action == 'approve':
            # 检查图书是否有库存
            if record.book.available <= 0:
                messages.error(request, '图书库存不足，无法批准借阅申请')
                return redirect('borrows:borrow_approval_list')
            
            # 批准借阅申请
            record.apply_status = 'approved'
            record.status = 'on'
            record.borrow_date = timezone.now()
            record.due_date = timezone.now() + timedelta(days=30)  # 30天后到期
            record.save()
            
            # 减少图书库存
            record.book.available -= 1
            record.book.save()
            
            messages.success(request, '借阅申请已批准')
        elif action == 'reject':
            # 拒绝借阅申请
            record.apply_status = 'rejected'
            record.save()
            messages.success(request, '借阅申请已拒绝')
        
        return redirect('borrows:borrow_approval_list')
    
    return render(request, 'borrows/borrow_approve.html', {'record': record, 'action': action})

@admin_required
def borrow_add(request):
    if request.method == 'POST':
        user_id = request.POST['user_id']
        book_id = request.POST['book_id']
        # 获取借阅数量，默认为1
        try:
            borrow_count = int(request.POST.get('borrow_count', 1))
            # 确保借阅数量至少为1
            borrow_count = max(1, borrow_count)
        except ValueError:
            borrow_count = 1
            
        # 获取图书并检查库存
        book = get_object_or_404(Book, pk=book_id)
        
        # 验证借阅数量是否超过可借数量
        if borrow_count > book.available:
            # 可以添加错误消息处理
            return redirect('borrows:borrow_list')
        
        # 为每本图书创建借阅记录
        for _ in range(borrow_count):
            BorrowRecord.objects.create(
                user_id=user_id, book_id=book_id,
                borrow_date=timezone.now(),
                due_date=timezone.now() + timedelta(days=30)
            )
        
        # 批量减少库存
        book.available -= borrow_count
        book.save()
        
        return redirect('borrows:borrow_list')
    users = User.objects.all()
    books = Book.objects.filter(available__gt=0)
    return render(request, 'borrows/borrow_form.html', {'users': users, 'books': books})

@admin_required
def return_request_list(request):
    # 管理员查看待确认的还书申请
    requested_records = BorrowRecord.objects.select_related('user', 'book').filter(
        return_request_status='requested'
    )
    return render(request, 'borrows/return_request_list.html', {'requested_records': requested_records})

@admin_required
def return_confirm(request, record_id):
    # 管理员确认还书
    record = get_object_or_404(BorrowRecord, pk=record_id, return_request_status='requested')
    
    if request.method == 'POST':
        # 确认还书
        record.status = 'off'
        record.return_date = timezone.now()
        record.return_request_status = 'confirmed'
        record.save()
        
        # 归还图书后增加库存
        record.book.available += 1
        record.book.save()
        
        messages.success(request, '还书确认成功')
        return redirect('borrows:return_request_list')
    
    return render(request, 'borrows/return_confirm.html', {'record': record})

@admin_required
def borrow_return(request, pk):
    # 管理员直接处理还书（保留原有功能，兼容直接还书）
    record = get_object_or_404(BorrowRecord, pk=pk, status='on')
    if request.method == 'POST':
        record.return_date = timezone.now()
        record.status = 'off'
        if hasattr(record, 'return_request_status') and record.return_request_status == 'requested':
            record.return_request_status = 'confirmed'
        record.save()
        # 恢复库存
        book = record.book
        book.available += 1
        book.save()
        messages.success(request, '还书处理成功')
        return redirect('borrows:borrow_list')
    return render(request, 'borrows/borrow_return.html', {'record': record})