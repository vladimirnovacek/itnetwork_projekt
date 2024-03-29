# Generated by Django 4.1.7 on 2023-03-16 14:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('insurance_app', '0005_product_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contract',
            name='payment',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='product',
            name='active',
            field=models.BooleanField(blank=True, default=True),
        ),
    ]
