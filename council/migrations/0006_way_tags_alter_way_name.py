# Generated by Django 5.1.2 on 2025-01-19 21:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('council', '0005_alter_way_oneway'),
    ]

    operations = [
        migrations.AddField(
            model_name='way',
            name='tags',
            field=models.TextField(default='{}'),
        ),
        migrations.AlterField(
            model_name='way',
            name='name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]