# Generated by Django 2.1.7 on 2020-08-25 19:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TestPlatform', '0003_duration_port'),
    ]

    operations = [
        migrations.AddField(
            model_name='duration',
            name='aet',
            field=models.CharField(blank=True, max_length=10, null=True, verbose_name='aet'),
        ),
    ]