# Generated by Django 5.1.4 on 2024-12-13 11:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0004_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='transaction_date',
            field=models.DateField(),
        ),
    ]
