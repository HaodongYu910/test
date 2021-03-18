# Generated by Django 2.1.7 on 2021-03-08 10:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TestPlatform', '0037_auto_20210303_1348'),
    ]

    operations = [
        migrations.CreateModel(
            name='install',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('server', models.CharField(blank=True, max_length=30, null=True, verbose_name='服务地址')),
                ('testcase', models.CharField(blank=True, max_length=30, null=True, verbose_name='测试数据')),
                ('version', models.CharField(blank=True, max_length=30, null=True, verbose_name='部署版本')),
                ('starttime', models.CharField(blank=True, max_length=30, null=True, verbose_name='部署时间')),
                ('hosdid', models.IntegerField(blank=True, null=True, verbose_name='hostid')),
                ('type', models.CharField(blank=True, max_length=30, null=True, verbose_name='类型')),
                ('status', models.BooleanField(default=False, verbose_name='状态')),
            ],
            options={
                'verbose_name': 'install',
                'verbose_name_plural': 'install',
                'db_table': 'install',
            },
        ),
    ]
