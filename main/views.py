from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.db.models import Count
from .models import Request, Category
from .forms import UserRegisterForm, RequestForm, RequestStatusForm
from django.http import JsonResponse

def index(request):
    solved_count = Request.objects.filter(status='solved').count()
    categories = Category.objects.annotate(request_count=Count('request'))
    return render(request, 'main/index.html', {
        'solved_count': solved_count,
        'categories': categories
    })

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Аккаунт создан! Теперь вы можете войти.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'main/register.html', {'form': form})

@login_required
def profile(request):
    user_requests = Request.objects.filter(user=request.user)
    return render(request, 'main/profile.html', {'requests': user_requests})

@login_required
def create_request(request):
    if request.method == 'POST':
        form = RequestForm(request.POST, request.FILES)
        if form.is_valid():
            request_obj = form.save(commit=False)
            request_obj.user = request.user
            request_obj.save()
            messages.success(request, 'Заявка успешно создана!')
            return redirect('profile')
    else:
        form = RequestForm()
    return render(request, 'main/create_request.html', {'form': form})

@login_required
def delete_request(request, pk):
    request_obj = get_object_or_404(Request, pk=pk, user=request.user)
    if request_obj.status == 'new':
        request_obj.delete()
        messages.success(request, 'Заявка успешно удалена!')
    else:
        messages.error(request, 'Нельзя удалить заявку, которая уже обработана!')
    return redirect('profile')

@staff_member_required
def admin_panel(request):
    requests = Request.objects.all()
    categories = Category.objects.all()
    return render(request, 'main/admin_panel.html', {
        'requests': requests,
        'categories': categories
    })

@staff_member_required
def update_request_status(request, pk):
    request_obj = get_object_or_404(Request, pk=pk)
    if request.method == 'POST':
        form = RequestStatusForm(request.POST, request.FILES, instance=request_obj)
        if form.is_valid():
            new_status = form.cleaned_data['status']
            if new_status == 'solved' and not form.cleaned_data['image_after']:
                messages.error(request, 'Для решенной заявки необходимо прикрепить фото!')
                return redirect('update_request_status', pk=pk)
            if new_status == 'rejected' and not form.cleaned_data['rejection_reason']:
                messages.error(request, 'Для отклоненной заявки необходимо указать причину!')
                return redirect('update_request_status', pk=pk)
            form.save()
            messages.success(request, 'Статус заявки обновлен!')
            return redirect('admin_panel')
    else:
        form = RequestStatusForm(instance=request_obj)
    return render(request, 'main/update_request_status.html', {
        'form': form,
        'request': request_obj
    })

@staff_member_required
def manage_categories(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        category_id = request.POST.get('category_id')
        
        if action == 'add':
            name = request.POST.get('name')
            if name:
                Category.objects.create(name=name)
                messages.success(request, 'Категория добавлена!')
        elif action == 'delete':
            category = get_object_or_404(Category, id=category_id)
            category.delete()
            messages.success(request, 'Категория удалена!')
            
    return redirect('admin_panel')

def get_solved_count(request):
    solved_count = Request.objects.filter(status='solved').count()
    return JsonResponse({'count': solved_count})
