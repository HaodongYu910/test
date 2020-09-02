# Generated by Django 2.1.7 on 2020-09-02 10:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TestPlatform', '0010_auto_20200901_1357'),
    ]

    operations = [
        migrations.AddField(
            model_name='duration',
            name='folder',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='dicom文件夹名称'),
        ),
        migrations.AddField(
            model_name='duration',
            name='pid',
            field=models.IntegerField(blank=True, null=True, verbose_name='进程号'),
        ),
    ]