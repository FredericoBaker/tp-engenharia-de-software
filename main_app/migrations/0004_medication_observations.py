# Generated by Django 5.0.1 on 2024-03-16 00:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0003_medication_next_dose_datetime'),
    ]

    operations = [
        migrations.AddField(
            model_name='medication',
            name='observations',
            field=models.TextField(blank=True, verbose_name='Observations'),
        ),
    ]
