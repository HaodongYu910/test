# Generated by Django 2.1.7 on 2021-01-04 13:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('TestPlatform', '0015_smoke'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='smoke',
            name='create_time',
        ),
        migrations.RemoveField(
            model_name='smoke',
            name='update_time',
        ),
    ]