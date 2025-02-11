from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Transaction(models.Model):

    TYPE_CHOICES = (
        ('income', 'Income'),
        ('expense', 'Expense'),
    )
    
    date = models.DateField(help_text="The date of the transaction")
    type = models.CharField(max_length=7, choices=TYPE_CHOICES, default='expense', help_text="Type of transaction, either income or expense")
    amount = models.DecimalField(max_digits=10, decimal_places=2, help_text="The monetary value of the transaction")
    category = models.ForeignKey('Category', related_name='transactions', on_delete=models.SET_NULL, null=True, blank=True, help_text="Category this transaction belongs to")
    description = models.TextField(blank=True, help_text="A brief description of the transaction")
    user = models.ForeignKey(User, related_name='transactions', on_delete=models.CASCADE, help_text="The user this transaction belongs to")

    def __str__(self):
        return f"{self.type.title()} of ${self.amount} on {self.date}"

