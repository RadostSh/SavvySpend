from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.db import models
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth import login
from .forms import RegisterUserForm, TransactionForm, CategoryForm, BudgetForm
from .models import Category, Transaction, Budget

@login_required(login_url='/login')
def index(request):
    """Welcome page."""
    total_income = Transaction.objects.filter(type='income').aggregate(models.Sum('amount'))['amount__sum'] or 0
    total_expense = Transaction.objects.filter(type='expense').aggregate(models.Sum('amount'))['amount__sum'] or 0
    balance = round(total_income - total_expense, 2)

    categories = Category.objects.all()

    context = {
        'username': request.user.username,
        'categories': categories,
        'balance': balance
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

    total_income = Transaction.objects.filter(type='income').aggregate(models.Sum('amount'))['amount__sum'] or 0
    total_expense = Transaction.objects.filter(type='expense').aggregate(models.Sum('amount'))['amount__sum'] or 0
    balance = round(total_income - total_expense, 2)

    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save()

            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'category': {
                        'id': category.id,
                        'name': category.name,
                    }
                })

    return render(request, 'index.html', {'form': form, 'categories': categories, 'balance': balance})


def list_categories(request):
    categories = Category.objects.all().order_by('name')
    return render(request, 'categories/list_categories.html', {'categories': categories})

def list_transactions(request):
    transactions = Transaction.objects.all().order_by('-date')
    return render(request, 'transactions/list_transactions.html', {'transactions': transactions})

def add_transaction(request):
    form = TransactionForm() 
    transactions = Transaction.objects.all().order_by('-date')

    total_income = Transaction.objects.filter(type='income').aggregate(models.Sum('amount'))['amount__sum'] or 0
    total_expense = Transaction.objects.filter(type='expense').aggregate(models.Sum('amount'))['amount__sum'] or 0
    balance = round(total_income - total_expense, 2)

    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save()
            
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
    
    return render(request, 'index.html', {'form': form, 'transactions': transactions, 'balance': balance})

def edit_transaction(request, transaction_id):
    transaction = get_object_or_404(Transaction, id=transaction_id)
    if request.method == 'POST':
        form = TransactionForm(request.POST, instance=transaction)
        if form.is_valid():
            form.save()
            return redirect('list_transactions')
    else:
        form = TransactionForm(instance=transaction)

    return render(request, 'transactions/edit_transaction.html', {'form': form, 'transaction': transaction})

def delete_transaction(request, transaction_id):
    transaction = get_object_or_404(Transaction, id=transaction_id)
    transaction.delete()

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'transaction_id': transaction_id,
            'message': 'Transaction deleted successfully.'
        })

    return redirect('transactions/list_transactions')

def delete_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    
    if request.method == 'POST':
        category.delete()

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': True, 'category_id': category_id})

    return redirect('list_categories')

def category_transactions(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    transactions = Transaction.objects.filter(category=category)

    return render(request, 'categories/category_transactions.html', {'category': category, 'transactions': transactions})

@login_required
def budget(request):
    user = request.user
    budgets = Budget.objects.filter(user=user).order_by('-created_at')

    if request.method == 'POST':
        form = BudgetForm(request.POST)
        if form.is_valid():
            budget = form.save(commit=False)
            budget.user = user
            budget.save()
            return redirect('budget')
    else:
        form = BudgetForm()

    # Calculation of the current balance
    total_income = Transaction.objects.filter(type='income').aggregate(models.Sum('amount'))['amount__sum'] or 0
    total_expense = Transaction.objects.filter(type='expense').aggregate(models.Sum('amount'))['amount__sum'] or 0
    balance = round(total_income - total_expense, 2)

    return render(request, 'budgets/budget.html', {'form': form, 'budgets': budgets, 'balance': balance})