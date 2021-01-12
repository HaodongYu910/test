# Generated by Django 2.1.7 on 2021-01-05 10:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TestPlatform', '0018_smoke_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='dicom',
            name='patientname',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='id'),
        ),
        migrations.AddField(
            model_name='dicom_record',
            name='patientname',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='id'),
        ),
        migrations.AddField(
            model_name='duration_record',
            name='patientname',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='id'),
        ),
        migrations.AlterField(
            model_name='dicom_record',
            name='patientid',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='id'),
        ),
    ]
