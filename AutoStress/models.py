from django.db import models
from AutoProject.models import Server

# Create your models here.


class stress(models.Model):
    """
      性能测试记录表
    """
    stressid = models.AutoField(primary_key=True)
    projectname = models.CharField(max_length=20, blank=True, null=True, verbose_name="项目名称")
    version = models.CharField(max_length=20, blank=True, null=True, verbose_name="测试版本")
    loadserver = models.CharField(max_length=40, blank=True, null=True, verbose_name="测试环境")
    testdata = models.CharField(max_length=400, blank=True, null=True, verbose_name="测试数据")
    thread = models.CharField(max_length=4, blank=True, null=True, verbose_name="线程数")
    synchroniz = models.CharField(max_length=4, blank=True, null=True, verbose_name="并发vu")
    ramp = models.CharField(max_length=4, blank=True, null=True, verbose_name="ramp up time")
    benchmark = models.IntegerField( blank=True, null=True, verbose_name="benchmark")
    single = models.CharField(max_length=4, blank=True, null=True, verbose_name="single")
    loop_count = models.CharField(max_length=4, blank=True, null=True, verbose_name="循环次数")
    duration = models.CharField(max_length=4, blank=True, null=True, verbose_name="持续时间")
    start_delay = models.CharField(max_length=4, blank=True, null=True, verbose_name="启动 秒")
    dicom_send = models.CharField(max_length=4, blank=True, null=True, verbose_name="duration 发送")
    start_date = models.CharField(max_length=20, blank=True, null=True, verbose_name="压测开始时间")
    end_date = models.CharField(max_length=20, blank=True, null=True, verbose_name="压测结束时间")
    loop_time = models.CharField(max_length=10, blank=True, null=True, verbose_name="执行时间")
    teststatus = models.CharField(max_length=20, blank=True, null=True, verbose_name="测试状态")
    jmeterstatus = models.BooleanField(default=True, verbose_name='jmeter状态')
    status = models.BooleanField(default=True, verbose_name='状态')
    Host = models.ForeignKey(Server, null=True, on_delete=models.CASCADE, verbose_name='Host')
    summary = models.TextField(max_length=2000, blank=True, null=True, verbose_name="结论")
    update_time = models.DateTimeField(auto_now=True, auto_now_add=False, verbose_name="修改时间")
    create_time = models.DateTimeField(auto_now=False, auto_now_add=True, verbose_name="创建时间")

    def __unicode__(self):
        return self.version

    class Meta:
        verbose_name = "性能测试记录表"
        verbose_name_plural = "性能测试记录表"
        db_table = 'stress'


class stress_record(models.Model):
    """
          压测记录表
        """
    id = models.AutoField(primary_key=True)
    version = models.CharField(max_length=30, blank=True, null=True, verbose_name="版本")
    studyuid = models.CharField(max_length=200, blank=True, null=True, verbose_name="uid")
    type = models.CharField(max_length=20, blank=True, null=True, verbose_name="类型")
    sec = models.CharField(max_length=20, blank=True, null=True, verbose_name="预测时间")
    start = models.CharField(max_length=50, blank=True, null=True, verbose_name="开始时间")
    end = models.CharField(max_length=50, blank=True, null=True, verbose_name="结束时间")
    job_time = models.CharField(max_length=20, blank=True, null=True, verbose_name="job预测时间")
    job_start = models.CharField(max_length=50, blank=True, null=True, verbose_name="job开始时间")
    job_end = models.CharField(max_length=50, blank=True, null=True, verbose_name="job结束时间")
    modelname = models.CharField(max_length=30, blank=True, null=True, verbose_name="模型名称")
    images = models.CharField(max_length=30, blank=True, null=True, verbose_name="张数")
    slicenumber = models.CharField(max_length=30, blank=True, null=True, verbose_name="层厚")
    aistatus = models.CharField(max_length=30, blank=True, null=True, verbose_name="预测状态")
    error = models.TextField(max_length=2000, blank=True, null=True, verbose_name="error")
    Stress = models.ForeignKey(stress, null=True, on_delete=models.CASCADE, verbose_name='Stress')
    Host = models.ForeignKey(Server, null=True, on_delete=models.CASCADE, verbose_name='Host')
    start_date = models.CharField(max_length=20, blank=True, null=True, verbose_name="压测开始时间")
    end_date = models.CharField(max_length=20, blank=True, null=True, verbose_name="压测结束时间")
    tps = models.FloatField(blank=True, null=True, verbose_name="压测tps")

    def __unicode__(self):
        return self.version

    class Meta:
        verbose_name = "压测结果记录表"
        verbose_name_plural = "压测结果记录表"
        db_table = 'stress_record'


class stress_result(models.Model):
    """
          压测结果记录表
        """
    id = models.AutoField(primary_key=True)
    version = models.CharField(max_length=10, blank=True, null=True, verbose_name="版本")
    modelname = models.CharField(max_length=30, blank=True, null=True, verbose_name="模型")
    type = models.CharField(max_length=15, blank=True, null=True, verbose_name="结果类型")
    slicenumber = models.CharField(max_length=6, blank=True, null=True, verbose_name="层厚")
    count = models.IntegerField(blank=True, null=True, verbose_name="次数")
    avg = models.CharField(max_length=10, blank=True, null=True, verbose_name="平均值")
    single = models.CharField(max_length=10, blank=True, null=True, verbose_name="单任务")
    median = models.CharField(max_length=10, blank=True, null=True, verbose_name="中间值")
    min = models.CharField(max_length=10, blank=True, null=True, verbose_name="最小时间")
    max = models.CharField(max_length=10, blank=True, null=True, verbose_name="最大时间")
    jobavg = models.CharField(max_length=10, blank=True, null=True, verbose_name="平均值")
    jobmedian = models.CharField(max_length=10, blank=True, null=True, verbose_name="中间值")
    jobmin = models.CharField(max_length=10, blank=True, null=True, verbose_name="最小时间")
    jobmax = models.CharField(max_length=10, blank=True, null=True, verbose_name="最大时间")
    coef = models.CharField(max_length=10, blank=True, null=True, verbose_name="系数")
    rate = models.TextField(max_length=10, blank=True, null=True, verbose_name="预测成功率")
    minimages = models.TextField(max_length=10, blank=True, null=True, verbose_name="影像张数")
    maximages = models.TextField(max_length=10, blank=True, null=True, verbose_name="影像张数")
    avgimages = models.TextField(max_length=10, blank=True, null=True, verbose_name="影像张数")
    Stress = models.ForeignKey(stress, null=True, on_delete=models.CASCADE, verbose_name='Stress')
    update_time = models.DateTimeField(auto_now=True, auto_now_add=False, verbose_name="修改时间")
    create_time = models.DateTimeField(auto_now=False, auto_now_add=True, verbose_name="创建时间")

    def __unicode__(self):
        return self.version

    class Meta:
        verbose_name = "压测结果记录表"
        verbose_name_plural = "压测结果记录表"
        db_table = 'stress_result'


class errorlog(models.Model):
    """
          压测错误日志记录表
        """
    id = models.AutoField(primary_key=True)
    version = models.CharField(max_length=10, blank=True, null=True, verbose_name="版本")
    content = models.TextField(max_length=2000, blank=True, null=True, verbose_name="错误内容")
    route = models.TextField(max_length=500, blank=True, null=True, verbose_name="路径")
    Stress = models.ForeignKey(stress, null=True, on_delete=models.CASCADE, verbose_name='Stress')

    def __unicode__(self):
        return self.version

    class Meta:
        verbose_name = "压测错误日志记录表"
        verbose_name_plural = "压测错误日志记录表"
        db_table = 'errorlog'
