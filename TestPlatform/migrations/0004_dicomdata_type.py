# Generated by Django 2.1.7 on 2020-11-24 17:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TestPlatform', '0003_auto_20201124_1215'),
    ]

    operations = [
        migrations.AddField(
            model_name='dicomdata',
            name='type',
            field=models.CharField(blank=True, max_length=10, null=True, verbose_name='类型'),
        ),
    ]
