# Generated by Django 5.0.1 on 2024-02-14 08:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0014_workingschedule'),
    ]

    operations = [
        migrations.CreateModel(
            name='Encounter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Prescription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(null=True)),
                ('width', models.PositiveIntegerField(default=210)),
                ('height', models.PositiveIntegerField(default=297)),
                ('background_image', models.ImageField(blank=True, null=True, upload_to='images/prescriptions/')),
                ('encounter', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='main.encounter')),
            ],
        ),
    ]