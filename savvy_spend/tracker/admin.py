from django.contrib import admin
from .models import Category, Transaction, Budget

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

admin.site.register(Category, CategoryAdmin)

class TransactionAdmin(admin.ModelAdmin):
    list_display = ('date', 'type', 'amount', 'category')
    list_filter = ('type', 'date', 'category')
    search_fields = ('description',)

admin.site.register(Transaction, TransactionAdmin)

class BudgetAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'created_at')
    search_fields = ('user__username',)

admin.site.register(Budget, BudgetAdmin)