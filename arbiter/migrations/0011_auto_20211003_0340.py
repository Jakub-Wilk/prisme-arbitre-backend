# Generated by Django 3.2.7 on 2021-10-03 01:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('arbiter', '0010_auto_20211002_1911'),
    ]

    operations = [
        migrations.AddField(
            model_name='arbiterprofile',
            name='birth_year',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='arbiterprofile',
            name='country',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='arbiterprofile',
            name='degree',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='arbiterprofile',
            name='votes',
            field=models.IntegerField(default=0),
        ),
    ]