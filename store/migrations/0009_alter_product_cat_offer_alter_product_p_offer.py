# Generated by Django 4.1.4 on 2023-03-23 16:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0008_alter_product_cat_offer_alter_product_p_offer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='cat_offer',
            field=models.FloatField(blank=True, default=None),
        ),
        migrations.AlterField(
            model_name='product',
            name='p_offer',
            field=models.FloatField(blank=True, default=None),
        ),
    ]
