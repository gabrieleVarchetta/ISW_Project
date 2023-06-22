# Generated by Django 3.2.5 on 2023-06-21 22:57

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0011_remove_paymentmethod_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='paymentmethod',
            name='default',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='paymentmethod',
            name='card_number',
            field=models.CharField(max_length=16, validators=[django.core.validators.MinLengthValidator(16)]),
        ),
    ]
