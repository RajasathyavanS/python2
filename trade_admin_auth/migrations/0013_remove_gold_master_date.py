# Generated by Django 2.2 on 2024-01-11 16:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('trade_admin_auth', '0012_gold_master_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='gold_master',
            name='date',
        ),
    ]
