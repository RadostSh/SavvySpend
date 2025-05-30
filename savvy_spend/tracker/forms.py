from django import forms
from .models import Transaction, Category, Budget, SavingGoal, Savings
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from datetime import datetime

class RegisterUserForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None
    class Meta:
        model = User
        fields = ("username", "first_name", "last_name",
                  "password1", "password2")

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Enter category name'}),
        }

    def __init__(self, *args, **kwargs):
        super(CategoryForm, self).__init__(*args, **kwargs)

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['date', 'type', 'amount', 'category', 'description']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'type': forms.Select(),
            'category': forms.Select(),
            'description': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super(TransactionForm, self).__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.all()

class BudgetForm(forms.ModelForm):
    class Meta:
        model = Budget
        fields = ['amount', 'month', 'year']
        widgets = {
            'amount': forms.NumberInput(attrs={'step': '0.01'}),
            'month': forms.Select(choices=[(i, i) for i in range(1, 13)]),
            'year': forms.Select(choices=[(y, y) for y in range(2020, datetime.now().year + 2)])
        }

class SavingGoalForm(forms.ModelForm):
    class Meta:
        model = SavingGoal
        fields = ['name', 'target_amount', 'current_amount', 'deadline']
        widgets = {
            'deadline': forms.DateInput(attrs={'type': 'date'}),
        }

class SavingsForm(forms.ModelForm):
    class Meta:
        model = Savings
        fields = ['amount']
        widgets = {
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter amount'})
        }