# Generated by Django 2.1.7 on 2020-12-04 14:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TestPlatform', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='stress_result',
            name='avgimages',
            field=models.TextField(blank=True, max_length=10, null=True, verbose_name='预测成功率'),
        ),
        migrations.AddField(
            model_name='stress_result',
            name='maximages',
            field=models.TextField(blank=True, max_length=10, null=True, verbose_name='预测成功率'),
        ),
        migrations.AddField(
            model_name='stress_result',
            name='minimages',
            field=models.TextField(blank=True, max_length=10, null=True, verbose_name='预测成功率'),
        ),
    ]