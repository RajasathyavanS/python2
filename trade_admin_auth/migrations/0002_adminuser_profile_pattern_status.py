# Generated by Django 2.2 on 2021-09-06 09:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trade_admin_auth', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='adminuser_profile',
            name='pattern_status',
            field=models.IntegerField(choices=[(0, 'Not Updated'), (1, 'Updated')], default=1, verbose_name='Pattern Status'),
        ),
    ]