# Generated by Django 4.1.4 on 2023-03-24 14:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0011_alter_product_cat_offer_alter_product_p_offer_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='image1',
            field=models.ImageField(null=True, upload_to='media'),
        ),
        migrations.AddField(
            model_name='product',
            name='image2',
            field=models.ImageField(null=True, upload_to='media'),
        ),
        migrations.AlterField(
            model_name='product',
            name='images',
            field=models.ImageField(null=True, upload_to='media'),
        ),
    ]
