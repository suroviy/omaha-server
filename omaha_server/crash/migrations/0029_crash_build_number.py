# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2017-04-17 06:46


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crash', '0028_crash_os'),
    ]

    operations = [
        migrations.AddField(
            model_name='crash',
            name='build_number',
            field=models.CharField(blank=True, max_length=32, null=True),
        ),
    ]
