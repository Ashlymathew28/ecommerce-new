# Generated by Django 4.1.4 on 2023-03-23 14:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0006_alter_product_cat_offer_alter_product_p_offer'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='user_price',
            field=models.FloatField(blank=True, default=0),
        ),
    ]
