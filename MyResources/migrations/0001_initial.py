# Generated by Django 2.0.1 on 2018-01-30 12:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Events',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('summary', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=100)),
                ('start_dateTime', models.CharField(max_length=50)),
                ('end_datTime', models.CharField(max_length=50)),
                ('location', models.CharField(max_length=100)),
                ('highlighted', models.TextField()),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='events', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Resources',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('resourceId', models.CharField(max_length=500, null=True)),
                ('resourceName', models.CharField(max_length=50)),
                ('generatedResourceName', models.CharField(max_length=100)),
                ('resourceType', models.CharField(max_length=10)),
                ('resourceEmail', models.CharField(max_length=100)),
                ('capacity', models.IntegerField()),
                ('resourceCategory', models.CharField(max_length=20)),
                ('highlighted', models.TextField()),
                ('events', models.ManyToManyField(blank=True, to='MyResources.Events')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='resource', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
