# Generated by Django 4.2.6 on 2023-11-08 13:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0011_alter_daily_hours_hours'),
    ]

    operations = [
        migrations.AlterField(
            model_name='daily_status',
            name='status_id',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
    ]
