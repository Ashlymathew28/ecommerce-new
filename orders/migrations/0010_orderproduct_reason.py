# Generated by Django 4.1.4 on 2023-04-17 06:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0009_alter_orderproduct_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderproduct',
            name='reason',
            field=models.CharField(max_length=1000, null=True),
        ),
    ]
