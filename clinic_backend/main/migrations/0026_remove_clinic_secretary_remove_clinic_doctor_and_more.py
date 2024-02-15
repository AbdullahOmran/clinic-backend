# Generated by Django 5.0.1 on 2024-02-15 16:37

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0025_doctor_last_opened_clinic_id_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='clinic',
            name='Secretary',
        ),
        migrations.RemoveField(
            model_name='clinic',
            name='doctor',
        ),
        migrations.RemoveField(
            model_name='doctor',
            name='last_opened_clinic_id',
        ),
        migrations.RemoveField(
            model_name='secretary',
            name='last_opened_clinic_id',
        ),
        migrations.AddField(
            model_name='doctor',
            name='clinic',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.clinic'),
        ),
        migrations.AddField(
            model_name='secretary',
            name='clinic',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.clinic'),
        ),
    ]
