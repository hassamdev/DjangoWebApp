# Generated by Django 4.2.6 on 2023-10-27 10:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0007_alter_employees_birth_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employees',
            name='image',
            field=models.ImageField(null=True, upload_to='images/'),
        ),
    ]
