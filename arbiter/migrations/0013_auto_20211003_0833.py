# Generated by Django 3.2.7 on 2021-10-03 06:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('arbiter', '0012_auto_20211003_0428'),
    ]

    operations = [
        migrations.AddField(
            model_name='arbiterprofile',
            name='verification_document',
            field=models.FileField(blank=True, null=True, upload_to='documents/'),
        ),
        migrations.DeleteModel(
            name='Document',
        ),
    ]
