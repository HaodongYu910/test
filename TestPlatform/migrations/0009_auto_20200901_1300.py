# Generated by Django 2.1.7 on 2020-09-01 13:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TestPlatform', '0008_auto_20200901_1250'),
    ]

    operations = [
        migrations.AlterField(
            model_name='duration_record',
            name='duration_id',
            field=models.IntegerField(blank=True, max_length=10, null=True, verbose_name='测试'),
        ),
    ]
