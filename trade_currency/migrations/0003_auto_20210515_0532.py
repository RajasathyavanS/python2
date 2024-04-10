

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('trade_currency', '0002_auto_20210129_1725'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='tradecurrency',
            options={'ordering': ['name'], 'verbose_name': 'TradeCurrency', 'verbose_name_plural': 'TradeCurrencys'},
        ),
        migrations.AlterModelOptions(
            name='tradepairs',
            options={'ordering': ['pair_name'], 'verbose_name': 'TradePairs', 'verbose_name_plural': 'TradePairs'},
        ),
    ]
