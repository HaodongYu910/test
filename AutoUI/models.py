from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
# Create your models here.


class autoui(models.Model):
    """
         autoui测试表
        """
    autoid = models.AutoField(primary_key=True)
    version = models.CharField(max_length=20, blank=True, null=True, verbose_name="版本")
    setup = models.CharField(max_length=20, blank=True, null=True, verbose_name="setup用例")
    cases = models.CharField(max_length=20, blank=True, null=True, verbose_name="用例")
    tearDown = models.CharField(max_length=20, blank=True, null=True, verbose_name="tearDown用例")
    progress = models.CharField(max_length=5, blank=True, null=True, verbose_name="进度")
    thread = models.CharField(max_length=5, blank=True, null=True, verbose_name="线程数")
    starttime = models.CharField(max_length=20, blank=True, null=True, verbose_name="开始预测时间")
    completiontime = models.CharField(max_length=20, blank=True, null=True, verbose_name="结束预测时间")
    total = models.CharField(max_length=5, blank=True, null=True, verbose_name="count")
    hostid = models.IntegerField(default=False, verbose_name='hostid')
    report = models.CharField(max_length=80, blank=True, null=True, verbose_name="报告")
    type = models.CharField(max_length=10, blank=True, null=True, verbose_name="类型")
    status = models.BooleanField(default=False, verbose_name='状态')

    def __unicode__(self):
        return self.autoid

    class Meta:
        verbose_name = "autoui测试表"
        verbose_name_plural = "autoui测试表"
        db_table = 'autoui'

class auto_uicase(models.Model):
    """
          auto_uicase 用例表
    """
    caseid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30, blank=True, null=True, verbose_name="名称")
    testdata = models.CharField(max_length=100, blank=True, null=True, verbose_name="关联测试数据")
    type = models.CharField(max_length=10, blank=True, null=True, verbose_name="类型")
    status = models.BooleanField(default=False, verbose_name='状态')
    update_time = models.DateTimeField(auto_now=True, auto_now_add=False, verbose_name="修改时间")
    create_time = models.DateTimeField(auto_now=False, auto_now_add=True, verbose_name="创建时间")

    def __unicode__(self):
        return self.caseid

    class Meta:
        verbose_name = "auto_uicase"
        verbose_name_plural = "auto_uicase"
        db_table = 'auto_uicase'

class auto_uirecord(models.Model):
    """
          auto_uirecord记录表
    """
    recordid = models.AutoField(primary_key=True)
    studyuid = models.CharField(max_length=200, blank=True, null=True, verbose_name="studyuid")
    vote = models.TextField(max_length=800, blank=True, null=True, verbose_name="挂载")
    expect = models.CharField(max_length=30, blank=True, null=True, verbose_name="预期结果")
    actual = models.CharField(max_length=30, blank=True, null=True, verbose_name="实际结果")
    aistatus = models.CharField(max_length=5, blank=True, null=True, verbose_name="预测结果")
    starttime = models.CharField(max_length=20, blank=True, null=True, verbose_name="开始时间")
    completiontime = models.CharField(max_length=20, blank=True, null=True, verbose_name="结束时间")
    result = models.TextField(max_length=2500, blank=True, null=True, verbose_name="结论")
    type = models.TextField(max_length=10, blank=True, null=True, verbose_name="类型")
    server = models.TextField(max_length=20, blank=True, null=True, verbose_name="服务")
    caseid = models.IntegerField(default=False, verbose_name='caseid')
    autoid = models.IntegerField(default=False, verbose_name='autoid')
    status = models.BooleanField(default=False, verbose_name='状态')
    update_time = models.DateTimeField(auto_now=True, auto_now_add=False, verbose_name="修改时间")
    create_time = models.DateTimeField(auto_now=False, auto_now_add=True, verbose_name="创建时间")

    def __unicode__(self):
        return self.recordid

    class Meta:
        verbose_name = "auto_uirecord"
        verbose_name_plural = "auto_uirecord"
        db_table = 'auto_uirecord'