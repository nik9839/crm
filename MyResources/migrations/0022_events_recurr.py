# Generated by Django 2.0.1 on 2018-03-05 07:35

from django.db import migrations
import recurrence.fields


class Migration(migrations.Migration):

    dependencies = [
        ('MyResources', '0021_auto_20180303_1551'),
    ]

    operations = [
        migrations.AddField(
            model_name='events',
            name='recurr',
            field=recurrence.fields.RecurrenceField(null=True),
        ),
    ]
