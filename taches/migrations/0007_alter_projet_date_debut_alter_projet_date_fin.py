# Generated by Django 5.1.5 on 2025-02-20 09:48

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('taches', '0006_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projet',
            name='date_debut',
            field=models.DateField(default=datetime.date(2025, 1, 1)),
        ),
        migrations.AlterField(
            model_name='projet',
            name='date_fin',
            field=models.DateField(default=datetime.date(2025, 12, 31)),
        ),
    ]
