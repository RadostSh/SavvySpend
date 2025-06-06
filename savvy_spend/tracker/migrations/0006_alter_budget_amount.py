# Generated by Django 5.1.4 on 2025-02-13 14:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0005_budget_year_alter_budget_amount_alter_budget_month_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='budget',
            name='amount',
            field=models.DecimalField(decimal_places=2, default=0, help_text='Total available budget', max_digits=10),
        ),
    ]
