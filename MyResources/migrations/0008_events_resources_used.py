# Generated by Django 2.0.1 on 2018-02-14 07:36

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MyResources', '0007_auto_20180210_1110'),
    ]

    operations = [
        migrations.AddField(
            model_name='events',
            name='resources_used',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=100), blank=True, default=[], size=None),
        ),
    ]
