# Generated by Django 5.1.2 on 2025-01-19 21:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('council', '0004_alter_way_nodes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='way',
            name='oneway',
            field=models.BooleanField(default=False),
        ),
    ]