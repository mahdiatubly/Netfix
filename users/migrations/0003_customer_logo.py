# Generated by Django 5.0 on 2024-01-20 04:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_userbase_groups_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='logo',
            field=models.ImageField(default='company_logos/default_logo.webp', upload_to='company_logos/'),
        ),
    ]
