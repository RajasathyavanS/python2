# Generated by Django 2.2 on 2024-01-08 17:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trade_admin_auth', '0008_auto_20240108_2310'),
    ]

    operations = [
        migrations.AddField(
            model_name='scheme_amount_master',
            name='Scheme_name',
            field=models.CharField(blank=True, max_length=250, null=True, verbose_name='Scheme Name'),
        ),
    ]