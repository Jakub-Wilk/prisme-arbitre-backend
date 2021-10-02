# Generated by Django 3.2.7 on 2021-10-02 15:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('arbiter', '0008_document'),
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('lat', models.FloatField(blank=True, null=True)),
                ('long', models.FloatField(blank=True, null=True)),
            ],
        ),
        migrations.AlterField(
            model_name='arbiterprofile',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='photos/'),
        ),
        migrations.AlterField(
            model_name='document',
            name='file',
            field=models.FileField(upload_to='documents/'),
        ),
        migrations.AlterField(
            model_name='language',
            name='arbiter',
            field=models.ManyToManyField(blank=True, related_name='languages', to='arbiter.ArbiterProfile'),
        ),
        migrations.AlterField(
            model_name='specialization',
            name='arbiter',
            field=models.ManyToManyField(blank=True, related_name='specializations', to='arbiter.ArbiterProfile'),
        ),
        migrations.AddField(
            model_name='arbiterprofile',
            name='location',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='arbiter.location'),
        ),
    ]