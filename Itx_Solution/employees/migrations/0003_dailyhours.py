# Generated by Django 4.2.6 on 2023-10-26 06:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0002_employees_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='dailyhours',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(unique=True)),
                ('hours', models.TimeField()),
                ('emp_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='employees.employees')),
            ],
        ),
    ]