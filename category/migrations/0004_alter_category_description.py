# Generated by Django 4.1.4 on 2022-12-31 09:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0003_alter_category_category_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='description',
            field=models.TextField(max_length=300, null=True),
        ),
    ]
