# Generated by Django 4.1.4 on 2023-04-07 17:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0007_alter_orderproduct_created_at_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderproduct',
            name='status',
            field=models.CharField(max_length=20, null=True),
        ),
    ]