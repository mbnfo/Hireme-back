# Generated by Django 4.2.6 on 2023-11-12 23:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0017_alter_notifications_model_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='notifications',
            name='seen',
            field=models.BooleanField(default=True),
        ),
    ]