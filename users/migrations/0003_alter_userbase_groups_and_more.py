# Generated by Django 5.0 on 2024-01-07 02:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('users', '0002_userbase_company_customer_delete_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userbase',
            name='groups',
            field=models.ManyToManyField(related_name='custom_user_set', to='auth.group'),
        ),
        migrations.AlterField(
            model_name='userbase',
            name='user_permissions',
            field=models.ManyToManyField(related_name='custom_user_set', to='auth.permission'),
        ),
    ]
