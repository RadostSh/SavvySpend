from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.db import models
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth import login
from django.db.models import Sum
from decimal import Decimal
from datetime import date
from .forms import RegisterUserForm, TransactionForm, CategoryForm, BudgetForm, SavingGoalForm
from .models import Category, Transaction, Budget, SavingGoal
from .currency import get_exchange_rate

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

@login_required
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

@login_required
def add_category(request):
    user = request.user
    form = CategoryForm()
    categories = Category.objects.all().order_by('name')

    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.user = user
            category.save()

            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'category': {
                        'id': category.id,
                        'name': category.name,
                    }
                })

    return render(request, 'index.html', {'form': form, 'categories': categories, 'balance': balance})

@login_required
def list_categories(request):
    categories = Category.objects.all().order_by('name')
    return render(request, 'categories/list_categories.html', {'categories': categories})

@login_required
def list_transactions(request):
    transactions = Transaction.objects.all().order_by('-date')
    return render(request, 'transactions/list_transactions.html', {'transactions': transactions})

@login_required
def add_transaction(request):
    user = request.user
    form = TransactionForm() 
    transactions = Transaction.objects.all().order_by('-date')

    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = user
            transaction.save()
            
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

@login_required
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

@login_required
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

@login_required
def delete_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    
    if request.method == 'POST':
        category.delete()

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True, 
                'category_id': category_id, 
                'message': 'Category deleted successfully.'})

    return redirect('list_categories')

@login_required
def category_transactions(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    transactions = Transaction.objects.filter(category=category)

    return render(request, 'categories/category_transactions.html', {'category': category, 'transactions': transactions})

@login_required
def budget(request):
    user = request.user
    current_month = date.today().month
    current_year = date.today().year

    monthly_budget, created = Budget.objects.get_or_create(
        user=user,
        month=current_month,
        year=current_year,
        defaults={'amount': 0}  
    )

    if request.method == 'POST':
        form = BudgetForm(request.POST, instance=monthly_budget)
        if form.is_valid():
            budget = form.save()

            return redirect('budget')

    else:
        form = BudgetForm(instance=monthly_budget)

    existing_budgets = Budget.objects.filter(user=user).order_by('-year', '-month')

    total_income = Transaction.objects.filter(
        user=user, type='income', date__month=current_month, date__year=current_year
    ).aggregate(Sum('amount'))['amount__sum'] or 0

    total_expense = Transaction.objects.filter(
        user=user, type='expense', date__month=current_month, date__year=current_year
    ).aggregate(Sum('amount'))['amount__sum'] or 0

    balance = round(total_income - total_expense, 2)

    for budget in existing_budgets:
        budget.total_income = Transaction.objects.filter(
            type='income', date__month=budget.month, date__year=budget.year
        ).aggregate(Sum('amount'))['amount__sum'] or 0

        budget.total_expense = Transaction.objects.filter(
            type='expense', date__month=budget.month, date__year=budget.year
        ).aggregate(Sum('amount'))['amount__sum'] or 0

        budget.difference = round(budget.total_income - budget.total_expense, 2)

    return render(request, 'budgets/budget.html', {
        'form': form,
        'total_income': total_income,
        'total_expense': total_expense,
        'balance': balance,
        'existing_budgets': existing_budgets
    })

@login_required
def savings(request):
    """Показва всички спестовни цели и форма за нова цел."""
    goals = SavingGoal.objects.filter(user=request.user).order_by('-created_at')

    if request.method == 'POST':
        form = SavingGoalForm(request.POST)
        if form.is_valid():
            goal = form.save(commit=False)
            goal.user = request.user
            goal.save()
            return redirect('savings')
    else:
        form = SavingGoalForm()

    return render(request, 'savings/savings.html', {'form': form, 'goals': goals})

@login_required
def add_to_savings(request, goal_id):
    """Добавяне на пари към спестената сума от баланса."""
    goal = get_object_or_404(SavingGoal, id=goal_id, user=request.user)

    if request.method == "POST":
        amount = request.POST.get("amount")

        try:
            amount = Decimal(amount)
            if amount > 0:
                total_income = Transaction.objects.filter(user=request.user, type='income').aggregate(Sum('amount'))['amount__sum'] or 0
                total_expense = Transaction.objects.filter(user=request.user, type='expense').aggregate(Sum('amount'))['amount__sum'] or 0
                current_balance = total_income - total_expense

                if amount > current_balance:
                    return redirect("savings")

                Transaction.objects.create(
                    user=request.user,
                    date=date.today(),
                    type='expense',
                    amount=amount,
                    category=None,
                    description=f"Transferred ${amount} to savings"
                )

                goal.current_amount += amount
                goal.save()

                return redirect("savings")

        except Exception as e:
            return redirect("savings")

    return redirect("savings")

def convert_currency(request):
    """Конвертира сума от една валута в друга."""
    if request.method == "GET":
        from_currency = request.GET.get("from")
        to_currency = request.GET.get("to")
        amount = request.GET.get("amount")

        if not from_currency or not to_currency or not amount:
            return JsonResponse({"error": "Missing parameters"}, status=400)
        
        try:
            amount = float(amount)
            rate = get_exchange_rate(from_currency, to_currency)
            
            if rate is None:
                return JsonResponse({"error": "Invalid currency or API error"}, status=400)

            converted_amount = round(amount * rate, 2)
            return JsonResponse({
                "success": True,
                "converted_amount": converted_amount,
                "rate": rate
            })

        except ValueError:
            return JsonResponse({"error": "Invalid amount"}, status=400)

    return JsonResponse({"error": "Invalid request"}, status=400)