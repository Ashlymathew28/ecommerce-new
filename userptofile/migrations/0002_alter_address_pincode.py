# Generated by Django 4.1.4 on 2023-03-20 04:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userptofile', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='pincode',
            field=models.IntegerField(),
        ),
    ]
