# Generated by Django 4.2.3 on 2023-10-12 11:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0016_product_offer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product_offer',
            name='discount',
            field=models.IntegerField(),
        ),
    ]
