# Generated by Django 5.0.1 on 2024-02-13 09:05

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_alter_patient_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]