# Generated by Django 2.1.7 on 2020-10-29 14:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TestPlatform', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='image',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('study_uid', models.CharField(blank=True, max_length=100, null=True, verbose_name='study_uid')),
            ],
            options={
                'verbose_name': 'image',
                'verbose_name_plural': 'image',
                'db_table': 'image',
            },
        ),
        migrations.RemoveField(
            model_name='duration',
            name='timer',
        ),
        migrations.AddField(
            model_name='duration',
            name='sleepcount',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='睡眠张数'),
        ),
        migrations.AddField(
            model_name='duration',
            name='sleeptime',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='睡眠时间'),
        ),
    ]