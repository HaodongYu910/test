# Generated by Django 2.1.7 on 2021-04-12 18:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AutoStress', '0002_stress_single'),
    ]

    operations = [
        migrations.AddField(
            model_name='stress',
            name='teststatus',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='测试状态'),
        ),
    ]
