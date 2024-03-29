# Generated by Django 5.0 on 2024-01-18 23:24

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40)),
                ('description', models.TextField()),
                ('price_hour', models.DecimalField(decimal_places=2, max_digits=100)),
                ('rating', models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)])),
                ('field', models.CharField(choices=[('Air Conditioner', 'Air Conditioner'), ('Carpentry', 'Carpentry'), ('Electricity', 'Electricity'), ('Gardening', 'Gardening'), ('Home Machines', 'Home Machines'), ('House Keeping', 'House Keeping'), ('Interior Design', 'Interior Design'), ('Locks', 'Locks'), ('Painting', 'Painting'), ('Plumbing', 'Plumbing'), ('Water Heaters', 'Water Heaters')], default='Air Conditioner', max_length=70)),
                ('requests_count', models.IntegerField(default=0)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.company')),
            ],
        ),
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
