# Generated by Django 5.1.4 on 2025-02-12 13:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0002_remove_category_description'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transaction',
            name='user',
        ),
    ]
