# Generated by Django 4.2.6 on 2023-10-31 12:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0010_alter_daily_hours_hours'),
    ]

    operations = [
        migrations.AlterField(
            model_name='daily_hours',
            name='hours',
            field=models.TimeField(),
        ),
    ]
