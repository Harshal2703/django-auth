# Generated by Django 5.1 on 2024-08-29 08:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0003_userinfo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='date_joined',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='last_updated',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
