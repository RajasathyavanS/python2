# Generated by Django 2.2 on 2024-01-06 19:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trade_admin_auth', '0005_auto_20240107_0025'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scheme',
            name='Scheme_type',
            field=models.IntegerField(choices=[(0, 'Amount'), (1, 'Weight')], default=0, verbose_name='Scheme Type'),
        ),
    ]