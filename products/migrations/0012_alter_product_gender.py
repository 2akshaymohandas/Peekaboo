# Generated by Django 4.2.3 on 2023-09-27 12:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0011_delete_color_remove_productvariant_color'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='gender',
            field=models.CharField(choices=[('male', 'Male'), ('female', 'Female')], max_length=10),
        ),
    ]
