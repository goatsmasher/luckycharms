# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-09 04:26
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20170109_0426'),
        ('events', '0002_remove_event_time_start'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location_name', models.CharField(max_length=50)),
                ('address_primary', models.CharField(max_length=50)),
                ('address_street', models.CharField(max_length=50)),
                ('address_city', models.CharField(max_length=50)),
                ('address_state', models.CharField(max_length=50)),
                ('postal_code', models.CharField(max_length=15)),
                ('address_neighborhood', models.CharField(max_length=50)),
                ('lng', models.CharField(max_length=50)),
                ('lat', models.CharField(max_length=50)),
                ('google_id', models.CharField(max_length=250)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.CharField(max_length=1000)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.User')),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.CharField(max_length=1000)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.User')),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='events.Event')),
            ],
        ),
        migrations.AddField(
            model_name='comment',
            name='related_message',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='events.Message'),
        ),
    ]
