# Generated by Django 2.1.7 on 2021-03-24 10:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('AutoTest', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='errorlog',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('version', models.CharField(blank=True, max_length=10, null=True, verbose_name='版本')),
                ('content', models.TextField(blank=True, max_length=2000, null=True, verbose_name='错误内容')),
                ('route', models.TextField(blank=True, max_length=500, null=True, verbose_name='路径')),
            ],
            options={
                'verbose_name': '压测错误日志记录表',
                'verbose_name_plural': '压测错误日志记录表',
                'db_table': 'errorlog',
            },
        ),
        migrations.CreateModel(
            name='stress',
            fields=[
                ('stressid', models.AutoField(primary_key=True, serialize=False)),
                ('projectname', models.CharField(blank=True, max_length=20, null=True, verbose_name='项目名称')),
                ('version', models.CharField(blank=True, max_length=20, null=True, verbose_name='测试版本')),
                ('loadserver', models.CharField(blank=True, max_length=40, null=True, verbose_name='测试环境')),
                ('testdata', models.CharField(blank=True, max_length=400, null=True, verbose_name='测试数据')),
                ('thread', models.CharField(blank=True, max_length=4, null=True, verbose_name='线程数')),
                ('synchroniz', models.CharField(blank=True, max_length=4, null=True, verbose_name='并发vu')),
                ('ramp', models.CharField(blank=True, max_length=4, null=True, verbose_name='ramp up time')),
                ('loop_count', models.CharField(blank=True, max_length=4, null=True, verbose_name='循环次数')),
                ('duration', models.CharField(blank=True, max_length=4, null=True, verbose_name='持续时间')),
                ('start_delay', models.CharField(blank=True, max_length=4, null=True, verbose_name='启动延时 秒')),
                ('dicom_send', models.CharField(blank=True, max_length=4, null=True, verbose_name='duration 发送')),
                ('start_date', models.CharField(blank=True, max_length=20, null=True, verbose_name='压测开始时间')),
                ('end_date', models.CharField(blank=True, max_length=20, null=True, verbose_name='压测结束时间')),
                ('loop_time', models.CharField(blank=True, max_length=10, null=True, verbose_name='执行时间')),
                ('jmeterstatus', models.BooleanField(default=True, verbose_name='jmeter状态')),
                ('status', models.BooleanField(default=True, verbose_name='状态')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='修改时间')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('Host', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='AutoTest.Server', verbose_name='Host')),
            ],
            options={
                'verbose_name': '性能测试记录表',
                'verbose_name_plural': '性能测试记录表',
                'db_table': 'stress',
            },
        ),
        migrations.CreateModel(
            name='stress_record',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('version', models.CharField(blank=True, max_length=30, null=True, verbose_name='版本')),
                ('studyuid', models.CharField(blank=True, max_length=200, null=True, verbose_name='uid')),
                ('type', models.CharField(blank=True, max_length=20, null=True, verbose_name='类型')),
                ('job_id', models.CharField(blank=True, max_length=80, null=True, verbose_name='id')),
                ('sec', models.CharField(blank=True, max_length=20, null=True, verbose_name='预测时间')),
                ('start', models.CharField(blank=True, max_length=50, null=True, verbose_name='开始时间')),
                ('end', models.CharField(blank=True, max_length=50, null=True, verbose_name='结束时间')),
                ('modelname', models.CharField(blank=True, max_length=30, null=True, verbose_name='模型名称')),
                ('images', models.CharField(blank=True, max_length=30, null=True, verbose_name='张数')),
                ('slicenumber', models.CharField(blank=True, max_length=30, null=True, verbose_name='层厚')),
                ('aistatus', models.CharField(blank=True, max_length=30, null=True, verbose_name='预测状态')),
                ('Stress', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='AutoStress.stress', verbose_name='Stress')),
            ],
            options={
                'verbose_name': '压测结果记录表',
                'verbose_name_plural': '压测结果记录表',
                'db_table': 'stress_record',
            },
        ),
        migrations.CreateModel(
            name='stress_result',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('version', models.CharField(blank=True, max_length=10, null=True, verbose_name='版本')),
                ('modelname', models.CharField(blank=True, max_length=30, null=True, verbose_name='模型')),
                ('type', models.CharField(blank=True, max_length=15, null=True, verbose_name='结果类型')),
                ('slicenumber', models.CharField(blank=True, max_length=6, null=True, verbose_name='层厚')),
                ('count', models.IntegerField(blank=True, null=True, verbose_name='次数')),
                ('avg', models.CharField(blank=True, max_length=10, null=True, verbose_name='平均值')),
                ('single', models.CharField(blank=True, max_length=10, null=True, verbose_name='单任务')),
                ('median', models.CharField(blank=True, max_length=10, null=True, verbose_name='中间值')),
                ('min', models.CharField(blank=True, max_length=10, null=True, verbose_name='最小时间')),
                ('max', models.CharField(blank=True, max_length=10, null=True, verbose_name='最大时间')),
                ('coef', models.CharField(blank=True, max_length=10, null=True, verbose_name='系数')),
                ('rate', models.TextField(blank=True, max_length=10, null=True, verbose_name='预测成功率')),
                ('minimages', models.TextField(blank=True, max_length=10, null=True, verbose_name='影像张数')),
                ('maximages', models.TextField(blank=True, max_length=10, null=True, verbose_name='影像张数')),
                ('avgimages', models.TextField(blank=True, max_length=10, null=True, verbose_name='影像张数')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='修改时间')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('Stress', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='AutoStress.stress', verbose_name='Stress')),
            ],
            options={
                'verbose_name': '压测结果记录表',
                'verbose_name_plural': '压测结果记录表',
                'db_table': 'stress_result',
            },
        ),
        migrations.AddField(
            model_name='errorlog',
            name='Stress',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='AutoStress.stress', verbose_name='Stress'),
        ),
    ]