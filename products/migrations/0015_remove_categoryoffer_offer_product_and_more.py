# Generated by Django 4.2.3 on 2023-10-03 11:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0014_categoryoffer'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='categoryoffer',
            name='offer_product',
        ),
        migrations.AddField(
            model_name='categoryoffer',
            name='offer_category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='products.category'),
        ),
    ]
