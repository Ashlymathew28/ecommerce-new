# Generated by Django 4.1.4 on 2023-03-14 04:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_remove_order_pay_id_remove_order_pay_method_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='pay_id',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='pay_method',
            field=models.CharField(default='Cash on delivery', max_length=100),
        ),
    ]