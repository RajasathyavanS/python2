# Generated by Django 2.2 on 2024-01-11 16:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trade_admin_auth', '0011_auto_20240111_2206'),
    ]

    operations = [
        migrations.AddField(
            model_name='gold_master',
            name='date',
            field=models.CharField(blank=True, max_length=250, null=True, verbose_name='date'),
        ),
    ]