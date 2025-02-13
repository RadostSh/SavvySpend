from django.db import models
from django.contrib.auth.models import User
from datetime import date

class Category(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='categories', null=True, blank=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Transaction(models.Model):

    TYPE_CHOICES = (
        ('income', 'Income'),
        ('expense', 'Expense'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions', null=True, blank=True)
    date = models.DateField(help_text="The date of the transaction")
    type = models.CharField(max_length=7, choices=TYPE_CHOICES, default='expense', help_text="Type of transaction, either income or expense")
    amount = models.DecimalField(max_digits=10, decimal_places=2, help_text="The monetary value of the transaction")
    category = models.ForeignKey('Category', related_name='transactions', on_delete=models.SET_NULL, null=True, blank=True, help_text="Category this transaction belongs to")
    description = models.TextField(blank=True, help_text="A brief description of the transaction")

    def __str__(self):
        return f"{self.type.title()} of ${self.amount} on {self.date}"

class Budget(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Един потребител може да има няколко бюджета
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0, help_text="Total available budget")
    month = models.IntegerField(default=date.today().month, help_text="Month of the budget")
    year = models.IntegerField(default=date.today().year, help_text="Year of the budget")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'month', 'year')  # Уникален бюджет за всеки месец

    def __str__(self):
        return f"Budget for {self.user.username} - {self.month}/{self.year}: ${self.amount}"

