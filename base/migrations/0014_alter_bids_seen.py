# Generated by Django 4.2.6 on 2023-11-11 19:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0013_alter_job_workers'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bids',
            name='seen',
            field=models.BooleanField(default=False),
        ),
    ]
