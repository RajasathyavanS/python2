

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trade_currency', '0003_auto_20210515_0532'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tradecurrency',
            name='balance_minimum',
            field=models.IntegerField(default=0, verbose_name='Balance Minimum'),
        ),
        migrations.AlterField(
            model_name='tradecurrency',
            name='lend_duration',
            field=models.IntegerField(default=0, verbose_name='Lend Duration'),
        ),
        migrations.AlterField(
            model_name='tradecurrency',
            name='lend_loanrate',
            field=models.IntegerField(default=0, verbose_name='Lend Rate'),
        ),
    ]
