# Generated by Django 2.1.7 on 2021-03-25 18:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AutoDicom', '0005_duration_version'),
    ]

    operations = [
        migrations.AddField(
            model_name='duration_record',
            name='diseases',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='预测类型'),
        ),
        migrations.AlterField(
            model_name='dicom',
            name='diseases',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='病种类型'),
        ),
    ]
