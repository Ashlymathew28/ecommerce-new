# Generated by Django 4.1.4 on 2023-01-03 08:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_alter_product_images'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='slug',
            new_name='prod_slug',
        ),
    ]