# Generated by Django 2.1.7 on 2021-04-19 17:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AutoStress', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='stress',
            name='benchmark',
            field=models.IntegerField(blank=True, null=True, verbose_name='benchmark'),
        ),
        migrations.AddField(
            model_name='stress',
            name='summary',
            field=models.TextField(blank=True, max_length=2000, null=True, verbose_name='结论'),
        ),
        migrations.AddField(
            model_name='stress_record',
            name='error',
            field=models.TextField(blank=True, max_length=2000, null=True, verbose_name='error'),
        ),
    ]