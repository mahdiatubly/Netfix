# Generated by Django 5.0 on 2024-01-27 03:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_alter_customer_logo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='logo',
            field=models.ImageField(default='customer_pictures/Customer_profile.webp', upload_to='customer_pictures/'),
        ),
    ]
