

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trade_currency', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tradecurrency',
            name='trans_min',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=16, verbose_name='Block Count '),
        ),
    ]
