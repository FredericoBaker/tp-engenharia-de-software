# Generated by Django 5.0.1 on 2024-03-15 23:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0002_medication'),
    ]

    operations = [
        migrations.AddField(
            model_name='medication',
            name='next_dose_datetime',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Next Dose Date and Time'),
        ),
    ]
