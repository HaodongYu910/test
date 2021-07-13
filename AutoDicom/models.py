from django.db import models

# Create your models here.
from AutoProject.models import Server, Project


class dicom(models.Model):
    """
          dicom数据表
        """
    id = models.AutoField(primary_key=True)
    patientid = models.CharField(max_length=50, blank=True, null=True, verbose_name="patientid")
    patientname = models.CharField(max_length=50, blank=True, null=True, verbose_name="id")
    studyinstanceuid = models.CharField(max_length=120, blank=True, null=True, verbose_name="数据uid")
    diseases = models.CharField(max_length=20, blank=True, null=True, verbose_name="病种类型")
    slicenumber = models.CharField(max_length=6, blank=True, null=True, verbose_name="肺炎层厚")
    imagecount = models.CharField(max_length=5, blank=True, null=True, verbose_name="张数")
    vote = models.CharField(max_length=800, blank=True, null=True, verbose_name="挂载")
    graphql = models.TextField(max_length=5000, blank=True, null=True, verbose_name="graphql")
    fileid = models.CharField(max_length=5, blank=True, null=True, verbose_name="文件ID")
    diagnosis = models.CharField(max_length=200, blank=True, null=True, verbose_name="诊断结果")
    predictor = models.CharField(max_length=5, blank=True, null=True, verbose_name="模型")
    type = models.CharField(max_length=10, blank=True, null=True, verbose_name="类型")
    route = models.CharField(max_length=100, blank=True, null=True, verbose_name="路径")
    status = models.BooleanField(default=False, verbose_name='状态')
    stressstatus = models.CharField(max_length=5, blank=True, null=True, verbose_name="性能状态")
    remark = models.CharField(max_length=50, blank=True, null=True, verbose_name="备注")
    update_time = models.DateTimeField(auto_now=True, auto_now_add=False, verbose_name="修改时间")
    create_time = models.DateTimeField(auto_now=False, auto_now_add=True, verbose_name="创建时间")

    def __unicode__(self):
        return self.studyinstanceuid

    class Meta:
        verbose_name = "dicom数据表"
        verbose_name_plural = "dicom数据表"
        db_table = 'dicom'

class dicom_detail(models.Model):
    """
      dicom数据 详情表
    """
    id = models.AutoField(primary_key=True)
    patientid = models.CharField(max_length=50, blank=True, null=True, verbose_name="patientid")
    patientname = models.CharField(max_length=50, blank=True, null=True, verbose_name="patientname")
    studyinstanceuid = models.CharField(max_length=120, blank=True, null=True, verbose_name="数据uid")
    SeriesInstanceUID = models.CharField(max_length=120, blank=True, null=True, verbose_name="数据uid")
    SOPInstanceUID = models.CharField(max_length=120, blank=True, null=True, verbose_name="数据uid")
    AccessionNumber = models.CharField(max_length=120, blank=True, null=True, verbose_name="数据uid")
    slice_thickness = models.CharField(max_length=10, blank=True, null=True, verbose_name="层厚")
    Modality = models.CharField(max_length=30, blank=True, null=True, verbose_name="层厚")
    route = models.CharField(max_length=120, blank=True, null=True, verbose_name="路径")
    status = models.BooleanField(default=True, verbose_name="0是关闭，1是启用")

    def __unicode__(self):
        return self.patientname

    class Meta:
        verbose_name = "dicom数据详情表"
        verbose_name_plural = "dicom数据详情表"
        db_table = 'dicom_detail'

class dicom_group(models.Model):
    """
        dicom 分组
    """
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, blank=True, null=True, verbose_name="名称")
    group = models.CharField(max_length=20, blank=True, null=True, verbose_name="组")
    amount = models.IntegerField(blank=True, null=True, verbose_name="数量")
    route = models.CharField(max_length=500, blank=True, null=True, verbose_name="路径")
    predictor = models.CharField(max_length=25, blank=True, null=True, verbose_name="模型类型")
    type = models.CharField(max_length=10, blank=True, null=True, verbose_name="类型")
    remark = models.CharField(max_length=50, blank=True, null=True, verbose_name="备注")
    project = models.ForeignKey(to=Project, null=True, on_delete=models.CASCADE, verbose_name='所属项目')
    status = models.BooleanField(default=False, verbose_name='状态')
    update_time = models.DateTimeField(auto_now=True, auto_now_add=False, verbose_name="修改时间")
    create_time = models.DateTimeField(auto_now=False, auto_now_add=True, verbose_name="创建时间")

    def __unicode__(self):
        return self.id

    class Meta:
        verbose_name = "dicom组表"
        verbose_name_plural = "dicom组表"
        db_table = 'dicom_group'


class dicom_group_detail(models.Model):
    """
          dicom 分组详情
        """
    id = models.AutoField(primary_key=True)
    dicom = models.ForeignKey(to=dicom, null=True, on_delete=models.CASCADE, verbose_name='id')
    group = models.ForeignKey(to=dicom_group, null=True, on_delete=models.CASCADE, verbose_name='id')
    status = models.BooleanField(default=False, verbose_name='状态')

    def __unicode__(self):
        return self.id

    class Meta:
        verbose_name = "dicom组表"
        verbose_name_plural = "dicom组表"
        db_table = 'dicom_group_detail'

class dicom_relation(models.Model):
    """
      提交记录，关系数据表
    """
    id = models.AutoField(primary_key=True)
    baseid = models.CharField(max_length=50, blank=True, null=True, verbose_name="dicom_group_id")
    custom = models.CharField(max_length=500, blank=True, null=True, verbose_name="哪次的补充数据")
    old_path = models.CharField(max_length=500, blank=True, null=True, verbose_name="提交数据时路劲")
    new_path = models.CharField(max_length=500, blank=True, null=True, verbose_name="新路径")
    success_uid = models.CharField(max_length=500, blank=True, null=True, verbose_name="成功的uid")
    fail_uid = models.CharField(max_length=500, blank=True, null=True, verbose_name="失败的uid")
    type = models.CharField(max_length=10, blank=True, null=True, verbose_name="类型")
    predictor = models.CharField(max_length=25, blank=True, null=True, verbose_name="模型类型")
    status = models.BooleanField(default=True, verbose_name="0是关闭，1是启用")
    update_time = models.DateTimeField(auto_now=True, auto_now_add=False, verbose_name="修改时间")
    create_time = models.DateTimeField(auto_now=False, auto_now_add=True, verbose_name="创建时间")

    def __unicode__(self):
        return self.old_path

    class Meta:
        verbose_name = "提交记录关系表"
        verbose_name_plural = "提交记录关系表"
        db_table = 'dicom_relation'


class duration(models.Model):
    """
          持续化测试记录表
        """
    id = models.AutoField(primary_key=True)
    version = models.CharField(max_length=20, blank=True, null=True, verbose_name="版本")
    server = models.CharField(max_length=20, blank=True, null=True, verbose_name="服务器ip")
    port = models.CharField(max_length=10, blank=True, null=True, verbose_name="服务器端口号")
    aet = models.CharField(max_length=20, blank=True, null=True, verbose_name="aet")
    patientid = models.CharField(max_length=50, blank=True, null=True, verbose_name="patientid")
    patientname = models.CharField(max_length=50, blank=True, null=True, verbose_name="patientname")
    dicom = models.CharField(max_length=500, blank=True, null=True, verbose_name="dicom数据")
    group = models.CharField(max_length=200, blank=True, null=True, verbose_name="组信息")
    sendcount = models.IntegerField(blank=True, null=True, verbose_name="共计发送")
    start_time = models.CharField(max_length=20, blank=True, null=True, verbose_name="开始时间")
    end_time = models.CharField(max_length=20, blank=True, null=True, verbose_name="结束时间")
    sleepcount = models.IntegerField(blank=True, null=True, verbose_name="睡眠张数")
    sleeptime = models.IntegerField(blank=True, null=True, verbose_name="睡眠时间")
    series = models.BooleanField(default=True, verbose_name='series')
    sendstatus = models.BooleanField(default=True, verbose_name='发送状态')
    status = models.BooleanField(default=False, verbose_name='状态')
    type = models.IntegerField(blank=True, null=True, verbose_name='发送类型')
    dds = models.CharField(max_length=20, blank=True, null=True,  verbose_name='dds 服务')
    Host = models.ForeignKey(to=Server, null=True, on_delete=models.CASCADE, verbose_name='Host')
    project = models.ForeignKey(to=Project, null=True, on_delete=models.CASCADE, verbose_name='所属项目')
    update_time = models.DateTimeField(auto_now=True, auto_now_add=False, verbose_name="修改时间")
    create_time = models.DateTimeField(auto_now=False, auto_now_add=True, verbose_name="创建时间")

    def __unicode__(self):
        return self.patientname

    class Meta:
        verbose_name = "持续化配置"
        verbose_name_plural = "持续化配置"
        db_table = 'duration'

class duration_record(models.Model):
    """
          持续化测试记录表
        """
    id = models.AutoField(primary_key=True)
    patientid = models.CharField(max_length=80, blank=True, null=True, verbose_name="patientid")
    patientname = models.CharField(max_length=50, blank=True, null=True, verbose_name="patientname")
    studyinstanceuid = models.CharField(max_length=200, blank=True, null=True, verbose_name="数据uid")
    studyolduid = models.CharField(max_length=200, blank=True, null=True, verbose_name="影像张数验证")
    image = models.IntegerField(blank=True, null=True, verbose_name="影像张数")
    image_receive = models.IntegerField(blank=True, null=True, verbose_name="接收影像张数")
    sec = models.DecimalField(max_digits=20, decimal_places=8, blank=True, null=True, verbose_name="预测时间")
    start = models.CharField(max_length=50, blank=True, null=True, verbose_name="开始时间")
    end = models.CharField(max_length=50, blank=True, null=True, verbose_name="结束时间")
    job_sec = models.DecimalField(max_digits=20, decimal_places=8, blank=True, null=True, verbose_name="job预测时间")
    job_start = models.CharField(max_length=50, blank=True, null=True, verbose_name="job开始时间")
    job_end = models.CharField(max_length=50, blank=True, null=True, verbose_name="job结束时间")
    error = models.TextField(max_length=3000, blank=True, null=True, verbose_name="error信息")
    slicenumber = models.CharField(max_length=30, blank=True, null=True, verbose_name="层厚")
    aistatus = models.CharField(max_length=10, blank=True, null=True, verbose_name="AI预测结果")
    diagnosis = models.TextField(max_length=500, blank=True, null=True, verbose_name="诊断结果")
    error = models.TextField(max_length=2000, blank=True, null=True, verbose_name="error")
    model = models.CharField(max_length=30, blank=True, null=True, verbose_name="模型")
    diseases = models.CharField(max_length=20, blank=True, null=True, verbose_name="病种")
    relation_id = models.CharField(max_length=20, blank=True, null=True, verbose_name='关联id')
    type = models.CharField(max_length=20, blank=True, null=True, verbose_name="类型")
    status = models.CharField(max_length=5, blank=True, null=True, verbose_name="状态")
    Host = models.ForeignKey(Server, null=True, on_delete=models.CASCADE, verbose_name='Host')
    update_time = models.DateTimeField(auto_now=True, auto_now_add=False, verbose_name="修改时间")
    create_time = models.DateTimeField(auto_now=False, auto_now_add=True, verbose_name="创建时间")

    def __unicode__(self):
        return self.studyinstanceuid

    class Meta:
        verbose_name = "持续化测试记录表"
        verbose_name_plural = "持续化测试记录表"
        db_table = 'duration_record'

