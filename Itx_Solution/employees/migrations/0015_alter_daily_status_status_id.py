# Generated by Django 4.2.6 on 2023-11-08 13:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0014_alter_daily_status_status_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='daily_status',
            name='status_id',
            field=models.IntegerField(primary_key=True, serialize=False, verbose_name='status_id'),
        ),
    ]
