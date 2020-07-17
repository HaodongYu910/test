# Generated by Django 2.1.7 on 2020-07-17 14:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TestPlatform', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='stress_data',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('patientid', models.CharField(blank=True, max_length=50, null=True, verbose_name='patientid')),
                ('studyinstanceuid', models.CharField(blank=True, max_length=100, null=True, verbose_name='数据uid')),
                ('diseases', models.CharField(blank=True, max_length=20, null=True, verbose_name='预测类型')),
                ('automatic', models.CharField(blank=True, max_length=5, null=True, verbose_name='自动或手动预测')),
                ('vote', models.CharField(blank=True, max_length=500, null=True, verbose_name='挂载')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='修改时间')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
            ],
            options={
                'verbose_name': '测试数据表',
                'verbose_name_plural': '测试数据表',
                'db_table': 'stress_data',
            },
        ),
        migrations.AddField(
            model_name='duration_record',
            name='time',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='测试'),
        ),
        migrations.AlterField(
            model_name='duration_record',
            name='accessionnumber',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='accessionnumber'),
        ),
        migrations.AlterField(
            model_name='duration_record',
            name='aistatus',
            field=models.CharField(blank=True, max_length=10, null=True, verbose_name='测试数据'),
        ),
        migrations.AlterField(
            model_name='duration_record',
            name='diagnosis',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='测试数据'),
        ),
        migrations.AlterField(
            model_name='duration_record',
            name='imagecount',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='测试'),
        ),
        migrations.AlterField(
            model_name='duration_record',
            name='imagecount_server',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='测试'),
        ),
        migrations.AlterField(
            model_name='duration_record',
            name='patientid',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='patientid'),
        ),
        migrations.AlterField(
            model_name='duration_record',
            name='sendserver',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='发送服务'),
        ),
        migrations.AlterField(
            model_name='duration_record',
            name='studyinstanceuid',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='数据uid'),
        ),
    ]
