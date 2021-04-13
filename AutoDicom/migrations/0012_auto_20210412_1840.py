# Generated by Django 2.1.7 on 2021-04-12 18:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('AutoDicom', '0011_auto_20210409_1536'),
    ]

    operations = [
        migrations.CreateModel(
            name='dicom_group',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=50, null=True, verbose_name='组名')),
                ('type', models.CharField(blank=True, max_length=10, null=True, verbose_name='类型')),
                ('remark', models.CharField(blank=True, max_length=50, null=True, verbose_name='备注')),
                ('status', models.BooleanField(default=False, verbose_name='状态')),
            ],
            options={
                'verbose_name': 'dicom组表',
                'verbose_name_plural': 'dicom组表',
                'db_table': 'dicom_group',
            },
        ),
        migrations.CreateModel(
            name='dicom_group_detail',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
            ],
            options={
                'verbose_name': 'dicom组表',
                'verbose_name_plural': 'dicom组表',
                'db_table': 'dicom_group_detail',
            },
        ),
        migrations.AddField(
            model_name='dicom',
            name='remark',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='备注'),
        ),
        migrations.AddField(
            model_name='dicom_group_detail',
            name='dicom',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='AutoDicom.dicom', verbose_name='id'),
        ),
        migrations.AddField(
            model_name='dicom_group_detail',
            name='group',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='AutoDicom.dicom_group', verbose_name='id'),
        ),
    ]
