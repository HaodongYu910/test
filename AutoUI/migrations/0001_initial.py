# Generated by Django 2.1.7 on 2021-03-22 16:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('AutoTest', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='auto_uicase',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=30, null=True, verbose_name='名称')),
                ('testdata', models.CharField(blank=True, max_length=100, null=True, verbose_name='关联测试数据')),
                ('type', models.CharField(blank=True, max_length=10, null=True, verbose_name='类型')),
                ('status', models.BooleanField(default=False, verbose_name='状态')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='修改时间')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
            ],
            options={
                'verbose_name': 'auto_uicase',
                'verbose_name_plural': 'auto_uicase',
                'db_table': 'auto_uicase',
            },
        ),
        migrations.CreateModel(
            name='auto_uirecord',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('studyuid', models.CharField(blank=True, max_length=200, null=True, verbose_name='studyuid')),
                ('vote', models.TextField(blank=True, max_length=800, null=True, verbose_name='挂载')),
                ('expect', models.CharField(blank=True, max_length=30, null=True, verbose_name='预期结果')),
                ('actual', models.CharField(blank=True, max_length=30, null=True, verbose_name='实际结果')),
                ('aistatus', models.CharField(blank=True, max_length=5, null=True, verbose_name='预测结果')),
                ('starttime', models.CharField(blank=True, max_length=20, null=True, verbose_name='开始时间')),
                ('completiontime', models.CharField(blank=True, max_length=20, null=True, verbose_name='结束时间')),
                ('result', models.TextField(blank=True, max_length=2500, null=True, verbose_name='结论')),
                ('type', models.CharField(blank=True, max_length=10, null=True, verbose_name='类型')),
                ('server', models.CharField(blank=True, max_length=20, null=True, verbose_name='服务')),
                ('status', models.BooleanField(default=False, verbose_name='状态')),
                ('dicomid', models.IntegerField(default=False, verbose_name='dicomid')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='修改时间')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
            ],
            options={
                'verbose_name': 'auto_uirecord',
                'verbose_name_plural': 'auto_uirecord',
                'db_table': 'auto_uirecord',
            },
        ),
        migrations.CreateModel(
            name='autoui',
            fields=[
                ('autoid', models.AutoField(primary_key=True, serialize=False)),
                ('version', models.CharField(blank=True, max_length=20, null=True, verbose_name='版本')),
                ('setup', models.CharField(blank=True, max_length=20, null=True, verbose_name='setup用例')),
                ('cases', models.CharField(blank=True, max_length=20, null=True, verbose_name='用例')),
                ('tearDown', models.CharField(blank=True, max_length=20, null=True, verbose_name='tearDown用例')),
                ('progress', models.CharField(blank=True, max_length=5, null=True, verbose_name='进度')),
                ('thread', models.CharField(blank=True, max_length=5, null=True, verbose_name='线程数')),
                ('starttime', models.CharField(blank=True, max_length=20, null=True, verbose_name='开始预测时间')),
                ('completiontime', models.CharField(blank=True, max_length=20, null=True, verbose_name='结束预测时间')),
                ('total', models.CharField(blank=True, max_length=5, null=True, verbose_name='count')),
                ('report', models.CharField(blank=True, max_length=80, null=True, verbose_name='报告')),
                ('type', models.CharField(blank=True, max_length=10, null=True, verbose_name='类型')),
                ('status', models.BooleanField(default=False, verbose_name='状态')),
                ('Host', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='AutoTest.Server', verbose_name='Host')),
            ],
            options={
                'verbose_name': 'autoui测试表',
                'verbose_name_plural': 'autoui测试表',
                'db_table': 'autoui',
            },
        ),
        migrations.AddField(
            model_name='auto_uirecord',
            name='auto',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='AutoUI.autoui', verbose_name='autouiid'),
        ),
        migrations.AddField(
            model_name='auto_uirecord',
            name='case',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='AutoUI.auto_uicase', verbose_name='autocaseid'),
        ),
    ]
