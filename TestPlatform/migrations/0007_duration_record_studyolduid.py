# Generated by Django 2.1.7 on 2020-08-26 15:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TestPlatform', '0006_auto_20200826_1156'),
    ]

    operations = [
        migrations.AddField(
            model_name='duration_record',
            name='studyolduid',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='原数据uid'),
        ),
    ]
