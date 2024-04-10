# Generated by Django 2.2 on 2022-10-10 07:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trade_currency', '0006_tradecurrency_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='tradecurrency',
            name='type_currncy',
            field=models.IntegerField(choices=[(0, 'coin'), (1, 'token')], default=0, verbose_name='Type Currncy'),
        ),
    ]