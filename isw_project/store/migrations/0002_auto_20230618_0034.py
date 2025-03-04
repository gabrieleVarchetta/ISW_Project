# Generated by Django 3.2.5 on 2023-06-18 00:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cartproduct',
            name='shopping_cart',
        ),
        migrations.AddField(
            model_name='shoppingcart',
            name='customer',
            field=models.OneToOneField(default=None, on_delete=django.db.models.deletion.CASCADE, to='store.customer'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='shoppingcart',
            name='products',
            field=models.ManyToManyField(to='store.CartProduct'),
        ),
    ]
