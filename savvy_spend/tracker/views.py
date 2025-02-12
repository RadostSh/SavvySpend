from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth import login
from .forms import RegisterUserForm, TransactionForm, CategoryForm
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

def add_category(request):
    form = CategoryForm()
    categories = Category.objects.all().order_by('name')
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save()

            # Проверка дали заявката идва от AJAX (JavaScript)
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'category': {
                        'id': category.id,
                        'name': category.name,
                    }
                })

    # Ако GET заявка - показва страницата с празна форма
    return render(request, 'index.html', {'form': form, 'categories': categories})


def list_categories(request):
    categories = Category.objects.all().order_by('name')  # Взема всички категории от базата
    return render(request, 'categories/list_categories.html', {'categories': categories})

def list_transactions(request):
    transactions = Transaction.objects.all().order_by('-date')  # Сортиране по дата в низходящ ред
    return render(request, 'transactions/list_transactions.html', {'transactions': transactions})

def add_transaction(request):
    form = TransactionForm()  # Дефинираме формата в началото
    transactions = Transaction.objects.all().order_by('-date')
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save()
            
            # Връщане на JSON отговор за AJAX заявка
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'transaction': {
                        'date': transaction.date.strftime('%Y-%m-%d'),
                        'type': transaction.get_type_display(),
                        'amount': str(transaction.amount),
                        'category': transaction.category.name if transaction.category else 'N/A',
                        'description': transaction.description,
                    }
                })
    
    return render(request, 'index.html', {'form': form, 'transactions': transactions})