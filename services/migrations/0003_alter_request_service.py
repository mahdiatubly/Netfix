# Generated by Django 5.0 on 2024-01-23 03:51

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0002_alter_request_customer_alter_request_service'),
    ]

    operations = [
        migrations.AlterField(
            model_name='request',
            name='service',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='services.service'),
        ),
    ]
