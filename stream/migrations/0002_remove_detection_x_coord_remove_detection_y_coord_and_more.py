# Generated by Django 5.1.2 on 2025-01-26 11:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stream', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='detection',
            name='x_coord',
        ),
        migrations.RemoveField(
            model_name='detection',
            name='y_coord',
        ),
        migrations.AddField(
            model_name='detection',
            name='x_max',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='detection',
            name='x_min',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='detection',
            name='y_max',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='detection',
            name='y_min',
            field=models.FloatField(default=0.0),
        ),
    ]