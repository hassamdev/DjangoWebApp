# Generated by Django 4.2.6 on 2023-10-26 08:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0005_daily_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employees',
            name='password',
            field=models.CharField(max_length=254, verbose_name='_password'),
        ),
    ]
