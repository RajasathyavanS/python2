# Generated by Django 2.2 on 2024-01-11 16:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trade_admin_auth', '0010_gold_master'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gold_master',
            name='Metal_id',
            field=models.CharField(blank=True, max_length=250, null=True, verbose_name='Metal Id'),
        ),
    ]
