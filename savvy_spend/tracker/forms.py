from django import forms
from .models import Transaction, Category, Budget
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

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
        fields = ['month', 'amount']
        widgets = {
            'month': forms.TextInput(attrs={'placeholder': 'Enter month, e.g., February 2025'}),
            'amount': forms.NumberInput(attrs={'placeholder': 'Enter budget amount'}),
        }