# Generated by Django 4.1.7 on 2023-03-19 20:33

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('insurance_app', '0010_insuredevent_processed'),
    ]

    operations = [
        migrations.AddField(
            model_name='insuredevent',
            name='reporting_date',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
