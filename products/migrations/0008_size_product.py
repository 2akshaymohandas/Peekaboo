# Generated by Django 4.2.3 on 2023-08-21 12:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0007_remove_size_product'),
    ]

    operations = [
        migrations.AddField(
            model_name='size',
            name='Product',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='products.product'),
        ),
    ]
