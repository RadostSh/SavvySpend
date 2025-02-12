from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.contrib.auth import login
from .forms import RegisterUserForm
from .models import Category, Transaction

@login_required(login_url='/login')
def index(request):
    """Welcome page."""
    context = {
        'username': request.user.username
    }
    return render(request, 'index.html', context)

def register(request):
    if request.method == "POST":
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(index)
    else:
        form = RegisterUserForm()
    context = {
        'form': form
    }
    return render(request, 'registration/register.html', context)

@require_http_methods(["POST"])
def add_category(request):
    category_name = request.POST.get('category_name', '').strip()
    if category_name:
        Category.objects.create(name=category_name)
        return JsonResponse({'success': True})
    
    return JsonResponse({'success': False, 'error': "The category name cannot be empty."})

def list_categories(request):
    categories = Category.objects.all()
    return render(request, 'categories.html', {'categories': categories})

def list_transactions(request):
    transactions = Transaction.objects.all().order_by('-date')  # Сортиране по дата в низходящ ред
    return render(request, 'transactions/list_transactions.html', {'transactions': transactions})