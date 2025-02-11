from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
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

def list_categories(request):
    categories = Category.objects.all()
    return render(request, 'categories/list_categories.html', {'categories': categories})

def list_transactions(request):
    transactions = Transaction.objects.all().order_by('-date')  # Сортиране по дата в низходящ ред
    return render(request, 'transactions/list_transactions.html', {'transactions': transactions})