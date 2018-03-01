# Generated by Django 2.0.1 on 2018-02-28 14:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MyResources', '0017_auto_20180228_0639'),
    ]

    operations = [
        migrations.AddField(
            model_name='events',
            name='end_date',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='events',
            name='recurrence',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='events',
            name='start_date',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='events',
            name='end_dateTime',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='events',
            name='start_dateTime',
            field=models.DateTimeField(null=True),
        ),
    ]