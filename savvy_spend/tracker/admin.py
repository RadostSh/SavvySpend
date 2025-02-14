from django.contrib import admin
from .models import Category, Transaction, Budget, SavingGoal

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'name',)
    search_fields = ('user__username',)

admin.site.register(Category, CategoryAdmin)

class TransactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'type', 'amount', 'category')
    list_filter = ('type', 'date', 'category')
    search_fields = ('user__username',)

admin.site.register(Transaction, TransactionAdmin)

class BudgetAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'created_at')
    search_fields = ('user__username',)

admin.site.register(Budget, BudgetAdmin)

class SavingGoalAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'target_amount', 'current_amount', 'deadline', 'created_at')
    search_fields = ('user__username',)

admin.site.register(SavingGoal, SavingGoalAdmin)