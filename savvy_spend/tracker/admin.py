from django.contrib import admin
from .models import Category, Transaction

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

admin.site.register(Category, CategoryAdmin)

class TransactionAdmin(admin.ModelAdmin):
    list_display = ('date', 'type', 'amount', 'category', 'user')
    list_filter = ('type', 'date', 'category')
    search_fields = ('description',)

admin.site.register(Transaction, TransactionAdmin)
