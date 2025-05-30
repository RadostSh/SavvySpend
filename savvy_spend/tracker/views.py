from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.db import models
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth import login
from django.db.models import Sum, Avg
from decimal import Decimal
from datetime import date, timedelta
from .forms import RegisterUserForm, TransactionForm, CategoryForm, BudgetForm, SavingGoalForm, SavingsForm
from .models import Category, Transaction, Budget, SavingGoal, Savings
from .currency import get_exchange_rate
from .utils import get_financial_advice

@login_required(login_url='/login')
def index(request):
    """Welcome page."""
    user = request.user
    today = date.today()

    total_income = Transaction.objects.filter(user=user, type='income').aggregate(Sum('amount'))['amount__sum'] or 0
    total_expense = Transaction.objects.filter(user=user, type='expense').aggregate(Sum('amount'))['amount__sum'] or 0
    balance = round(total_income - total_expense, 2)

    categories = Category.objects.filter(user=user).all()

    total_savings = Savings.objects.filter(user=user).aggregate(Sum('amount'))['amount__sum'] or 0

    last_six_months = today - timedelta(days=180)
    total_income = Transaction.objects.filter(
        user=user, type='income', date__gte=last_six_months
    ).aggregate(Sum('amount'))['amount__sum'] or 0

    total_expense = Transaction.objects.filter(
        user=user, type='expense', date__gte=last_six_months
    ).aggregate(Sum('amount'))['amount__sum'] or 0

    avg_savings_per_month = round((total_income - total_expense) / 6, 2) if total_income > total_expense else 0
    predicted_savings = avg_savings_per_month if avg_savings_per_month > 0 else 0

    context = {
        'username': request.user.username,
        'categories': categories,
        'balance': balance,
        'total_savings': total_savings,
        'avg_savings_per_month': avg_savings_per_month,
        'predicted_savings': predicted_savings
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

@login_required(login_url='/login')
def add_category(request):
    user = request.user
    form = CategoryForm()

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

@login_required(login_url='/login')
def list_categories(request):
    user = request.user
    categories = Category.objects.filter(user=user).all().order_by('name')
    return render(request, 'categories/list_categories.html', {'categories': categories})

@login_required(login_url='/login')
def list_transactions(request):
    user = request.user
    transactions = Transaction.objects.filter(user=user).all().order_by('-date')
    return render(request, 'transactions/list_transactions.html', {'transactions': transactions})

@login_required(login_url='/login')
def add_transaction(request):
    user = request.user
    form = TransactionForm() 

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
    
    return render(request, 'index.html', {'form': form, 'transactions': transaction})

@login_required(login_url='/login')
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

@login_required(login_url='/login')
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

@login_required(login_url='/login')
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

@login_required(login_url='/login')
def category_transactions(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    transactions = Transaction.objects.filter(category=category)

    return render(request, 'categories/category_transactions.html', {'category': category, 'transactions': transactions})

@login_required(login_url='/login')
def budget(request):
    user = request.user
    current_month = date.today().month
    current_year = date.today().year

    try:
        monthly_budget = Budget.objects.get(user=user, month=current_month, year=current_year)
    except Budget.DoesNotExist:
        monthly_budget = None

    if request.method == 'POST':
        form = BudgetForm(request.POST, instance=monthly_budget)
        if form.is_valid():
            budget = form.save(commit=False)
            budget.user = user
            budget.save()

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

        if budget.amount > 0:
            budget.expense_percentage = round((budget.total_expense / budget.amount) * 100, 2)
        else:
            budget.expense_percentage = 0

    return render(request, 'budgets/budget.html', {
        'form': form,
        'total_income': total_income,
        'total_expense': total_expense,
        'balance': balance,
        'existing_budgets': existing_budgets
    })

@login_required(login_url='/login')
def savings(request):
    """Show all savings goals and a form for a new goal."""
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

@login_required(login_url='/login')
def add_to_savings(request, goal_id):
    """Add money to your saved balance."""
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

@login_required(login_url='/login')
def convert_currency(request):
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

@login_required(login_url='/login')
def savings_forecast(request):
    """Predict future saving and allow recording new ones"""
    user = request.user
    today = date.today()

    total_savings = Savings.objects.filter(user=user).aggregate(Sum('amount'))['amount__sum'] or 0

    last_six_months = today - timedelta(days=180)
    total_income = Transaction.objects.filter(
        user=user, type='income', date__gte=last_six_months
    ).aggregate(Sum('amount'))['amount__sum'] or 0

    total_expense = Transaction.objects.filter(
        user=user, type='expense', date__gte=last_six_months
    ).aggregate(Sum('amount'))['amount__sum'] or 0

    avg_savings_per_month = round((total_income - total_expense) / 6, 2) if total_income > total_expense else 0
    predicted_savings = avg_savings_per_month if avg_savings_per_month > 0 else 0

    if request.method == "POST":
        form = SavingsForm(request.POST)
        if form.is_valid():
            savings = form.save(commit=False)
            savings.user = user
            savings.save()
            return redirect('savings_forecast')

    else:
        form = SavingsForm()

    return render(request, 'savings/savings_forecast.html', {
        'form': form,
        'total_savings': total_savings,
        'avg_savings_per_month': avg_savings_per_month,
        'predicted_savings': predicted_savings,
    })

def generate_financial_advice(request):

    user = request.user
    today = date.today()
    # Take all user savings
    total_savings = Savings.objects.filter(user=user).aggregate(Sum('amount'))['amount__sum'] or 0

    # Take all income and expenses for the last 6 months
    last_six_months = today - timedelta(days=180)
    total_income = Transaction.objects.filter(
        user=user, type='income', date__gte=last_six_months
    ).aggregate(Sum('amount'))['amount__sum'] or 0

    total_expense = Transaction.objects.filter(
        user=user, type='expense', date__gte=last_six_months
    ).aggregate(Sum('amount'))['amount__sum'] or 0

    avg_savings_per_month = round((total_income - total_expense) / 6, 2) if total_income > total_expense else 0
    predicted_savings = avg_savings_per_month if avg_savings_per_month > 0 else 0

    financial_advice = get_financial_advice(avg_savings_per_month, total_expense / 6, total_income / 6)

    return JsonResponse({'financial_advice': financial_advice})