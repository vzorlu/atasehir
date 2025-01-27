# Generated by Django 5.1.2 on 2025-01-27 11:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('notification', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='StreamImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='stream_images/')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('processed', models.BooleanField(default=False)),
                ('lang', models.FloatField(blank=True, null=True)),
                ('long', models.FloatField(blank=True, null=True)),
                ('fulladdress', models.TextField(blank=True, null=True)),
                ('area', models.CharField(blank=True, max_length=255, null=True)),
                ('deviceuuid', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Detection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('class_name', models.CharField(max_length=100)),
                ('x_min', models.FloatField(default=0.0)),
                ('y_min', models.FloatField(default=0.0)),
                ('x_max', models.FloatField(default=0.0)),
                ('y_max', models.FloatField(default=0.0)),
                ('confidence', models.FloatField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('notification', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='detections', to='notification.notification')),
                ('image', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='detections', to='stream.streamimage')),
            ],
        ),
    ]
