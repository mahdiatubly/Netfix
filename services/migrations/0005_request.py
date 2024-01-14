# Generated by Django 5.0 on 2024-01-13 13:10

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0004_remove_service_completed_remove_service_customers_and_more'),
        ('users', '0002_alter_userbase_groups_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Request',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('date', models.DateTimeField(auto_now=True)),
                ('completed', models.BooleanField(default=False)),
                ('rating', models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)])),
                ('customer', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='users.customer')),
                ('service', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='services.service')),
            ],
        ),
    ]
