

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trade_currency', '0004_auto_20210609_1058'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tradecurrency',
            name='balance_minimum',
            field=models.IntegerField(default=0, verbose_name='Maximum Leverage'),
        ),
    ]
