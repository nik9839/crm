# Generated by Django 2.0.1 on 2018-02-22 09:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MyResources', '0009_auto_20180220_0847'),
    ]

    operations = [
        migrations.AddField(
            model_name='resources',
            name='syncToken',
            field=models.CharField(blank=True, max_length=30),
        ),
    ]
