# Generated by Django 2.1.7 on 2021-02-08 10:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TestPlatform', '0031_auto_20210127_1539'),
    ]

    operations = [
        migrations.AddField(
            model_name='dicom',
            name='graphql',
            field=models.TextField(blank=True, max_length=5000, null=True, verbose_name='graphql'),
        ),
    ]
