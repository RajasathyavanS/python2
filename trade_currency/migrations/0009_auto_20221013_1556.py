# Generated by Django 2.2 on 2022-10-13 10:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trade_currency', '0008_tradecurrency_chain_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tradecurrency',
            name='chain_id',
            field=models.IntegerField(default=97, verbose_name='Chain ID'),
        ),
    ]
