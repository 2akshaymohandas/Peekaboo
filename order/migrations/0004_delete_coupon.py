# Generated by Django 4.2.3 on 2023-09-16 10:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0003_coupon'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Coupon',
        ),
    ]
