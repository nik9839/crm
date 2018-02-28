# Generated by Django 2.0.1 on 2018-02-26 12:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MyResources', '0015_auto_20180226_1214'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='resources',
            name='roomName',
        ),
        migrations.AlterField(
            model_name='resources',
            name='buildingId',
            field=models.CharField(blank=True, max_length=30),
        ),
        migrations.AlterField(
            model_name='resources',
            name='floorName',
            field=models.CharField(blank=True, max_length=30),
        ),
        migrations.AlterField(
            model_name='resources',
            name='resourceName',
            field=models.CharField(blank=True, max_length=30),
        ),
        migrations.AlterField(
            model_name='resources',
            name='resourceType',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='resources',
            name='syncToken',
            field=models.CharField(blank=True, max_length=40),
        ),
    ]
