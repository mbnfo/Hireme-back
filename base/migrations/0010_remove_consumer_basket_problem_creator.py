# Generated by Django 4.2.6 on 2023-11-10 23:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0009_alter_worker_cv'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='consumer',
            name='basket',
        ),
        migrations.AddField(
            model_name='problem',
            name='creator',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='base.consumer'),
        ),
    ]