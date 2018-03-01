# Generated by Django 2.0.1 on 2018-02-28 14:10

from django.db import migrations, models

from django.utils import timezone

def edit_null_items(apps, schema_editor):
    Events = apps.get_model("MyResources", "Events")
    for event in Events.objects.all():
        if event.start_dateTime ==None:
            event.start_dateTime = timezone.now().replace(year=1900)
            event.end_dateTime = timezone.now().replace(year=1901)
            event.save()



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
        migrations.RunPython(migrations.RunPython.noop, edit_null_items)
    ]
