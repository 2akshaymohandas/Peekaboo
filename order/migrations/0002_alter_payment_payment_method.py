# Generated by Django 4.2.3 on 2023-09-05 13:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='payment_method',
            field=models.CharField(choices=[('COD', 'COD')], max_length=100),
        ),
    ]
