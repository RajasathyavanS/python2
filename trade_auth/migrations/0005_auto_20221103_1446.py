# Generated by Django 2.2 on 2022-11-03 09:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('trade_currency', '0009_auto_20221013_1556'),
        ('trade_auth', '0004_auto_20221007_1542'),
    ]

    operations = [
        migrations.AddField(
            model_name='useraddress',
            name='select_id',
            field=models.CharField(blank=True, max_length=120, null=True, verbose_name='Select Id'),
        ),
        migrations.AddField(
            model_name='useraddress',
            name='select_token',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='Select_token', to='trade_currency.TradeCurrency', verbose_name='Select Token'),
            preserve_default=False,
        ),
    ]
