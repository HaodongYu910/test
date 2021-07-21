from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

HTTP_CHOICE = (
    ('HTTP', 'HTTP'),
    ('HTTPS', 'HTTPS')
)

REQUEST_TYPE_CHOICE = (
    ('POST', 'POST'),
    ('GET', 'GET'),
    ('PUT', 'PUT'),
    ('DELETE', 'DELETE')
)

REQUEST_PARAMETER_TYPE_CHOICE = (
    ('form-data', '表单(form-data)'),
    ('raw', '源数据(raw)'),
    ('Restful', 'Restful')
)

PARAMETER_TYPE_CHOICE = (
    ('text', 'text'),
    ('file', 'file')
)

HTTP_CODE_CHOICE = (
    ('200', '200'),
    ('404', '404'),
    ('400', '400'),
    ('502', '502'),
    ('500', '500'),
    ('302', '302'),
)

EXAMINE_TYPE_CHOICE = (
    ('no_check', '不校验'),
    ('only_check_status', '校验http状态'),
    ('json', 'JSON校验'),
    ('entirely_check', '完全校验'),
    ('Regular_check', '正则校验'),
)

UNIT_CHOICE = (
    ('m', '分'),
    ('h', '时'),
    ('d', '天'),
    ('w', '周'),
)

RESULT_CHOICE = (
    ('PASS', '成功'),
    ('FAIL', '失败'),
)

TASK_CHOICE = (
    ('circulation', '循环'),
    ('timing', '定时'),
)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


# ==================扩展用户====================================
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='用户', related_name='user')
    phone = models.CharField(max_length=11, default='', blank=True, verbose_name='手机号')
    mail = models.CharField(max_length=50, default='', blank=True, verbose_name='邮件')
    roles = models.CharField(max_length=10, default='', blank=True, verbose_name='角色')
    userphoto = models.CharField(max_length=100, default='', blank=True, verbose_name='头像')

    def __unicode__(self):
        return self.user.username

    def __str__(self):
        return self.phone


class Project(models.Model):
    """
    项目表
    """
    ProjectType = (
        ('Web', 'Web'),
        ('App', 'App')
    )

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, verbose_name='项目名称')
    version = models.CharField(max_length=20, blank=True, null=True, verbose_name="版本")
    type = models.CharField(max_length=50, verbose_name='类型', choices=ProjectType)
    status = models.BooleanField(default=True, verbose_name='状态')
    start_date = models.DateTimeField(auto_now=False, auto_now_add=False, null=True, blank=True, verbose_name="项目开始时间")
    end_date = models.DateTimeField(auto_now=False, auto_now_add=False, null=True, blank=True, verbose_name="发布日期")
    client = models.CharField(max_length=2, blank=True, null=True, verbose_name="0 是安卓 1是ios  2 是all")
    projectstatus = models.CharField(default="未開始", max_length=10, verbose_name="项目状态")
    description = models.CharField(max_length=1024, blank=True, null=True, verbose_name='描述')
    LastUpdateTime = models.DateTimeField(auto_now=True, verbose_name='最近修改时间')
    createTime = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, max_length=1024, verbose_name='创建人')

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '项目'
        verbose_name_plural = '项目'
        db_table = 'Project'


class project_version(models.Model):
    """
          项目版本
        """
    id = models.AutoField(primary_key=True)
    version = models.CharField(max_length=50, blank=True, null=True, verbose_name="版本")
    branch = models.CharField(max_length=20, blank=True, null=True, verbose_name="分支")
    package_name = models.CharField(max_length=50, blank=True, null=True, verbose_name="包名")
    path = models.TextField(max_length=1000, blank=True, null=True, verbose_name="路径")
    type = models.CharField(max_length=20, blank=True, null=True, verbose_name="类型 -1、 删除  2、保存")
    project = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name='所属项目')
    status = models.BooleanField(default=False, verbose_name='状态')
    update_time = models.DateTimeField(auto_now=True, verbose_name='修改时间')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    def __unicode__(self):
        return self.id

    class Meta:
        verbose_name = "project_version"
        verbose_name_plural = "project_version"
        db_table = 'project_version'


class ProjectDynamic(models.Model):
    """
    项目动态
    """
    id = models.AutoField(primary_key=True)
    project = models.ForeignKey(Project, related_name='dynamic_project', on_delete=models.CASCADE, verbose_name='所属项目')
    time = models.DateTimeField(max_length=128, verbose_name='操作时间')
    type = models.CharField(max_length=50, verbose_name='操作类型')
    operationObject = models.CharField(max_length=50, verbose_name='操作对象')
    user = models.ForeignKey(User, blank=True, null=True, related_name='userName',
                             on_delete=models.SET_NULL, verbose_name='操作人')
    description = models.CharField(max_length=1024, blank=True, null=True, verbose_name='描述')

    def __unicode__(self):
        return self.type

    class Meta:
        verbose_name = '项目动态'
        verbose_name_plural = '项目动态'
        db_table = 'ProjectDynamic'


class ProjectMember(models.Model):
    """
    项目成员
    """
    CHOICES = (
        ('超级管理员', '超级管理员'),
        ('开发', '开发'),
        ('测试', '测试'),
        ('运维', '运维'),
        ('PM', 'PM')
    )
    id = models.AutoField(primary_key=True)
    permissionType = models.CharField(max_length=50, verbose_name='权限角色', choices=CHOICES)
    project = models.ForeignKey(Project, related_name='member_project', on_delete=models.CASCADE, verbose_name='所属项目')
    user = models.ForeignKey(User, related_name='member_user', on_delete=models.CASCADE, verbose_name='用户')

    def __unicode__(self):
        return self.permissionType

    def __str__(self):
        return self.permissionType

    class Meta:
        verbose_name = '项目成员'
        verbose_name_plural = '项目成员'
        db_table = 'ProjectMember'


class Server(models.Model):
    """
    host域名
    """
    id = models.AutoField(primary_key=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name='项目')
    name = models.CharField(max_length=50, verbose_name='名称')
    host = models.CharField(max_length=50, verbose_name='Host地址')
    port = models.CharField(max_length=10, verbose_name='port')
    protocol = models.CharField(max_length=10, blank=True, null=True, verbose_name='协议')
    user = models.CharField(max_length=20, verbose_name='用户名')
    pwd = models.CharField(max_length=50, verbose_name='密码')
    remarks = models.CharField(max_length=50, verbose_name='备注')
    description = models.CharField(max_length=1024, blank=True, null=True, verbose_name='描述')
    status = models.BooleanField(default=True, verbose_name='状态')

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

    def __int__(self):
        return self.host

    class Meta:
        verbose_name = 'Server'
        verbose_name_plural = 'Server管理'
        db_table = 'Server'


class dictionary(models.Model):
    """
          dictionary 表
        """
    id = models.AutoField(primary_key=True)
    key = models.CharField(max_length=50, blank=True, null=True, verbose_name="key")
    value = models.CharField(max_length=2500, blank=True, null=True, verbose_name="value")
    remarks = models.CharField(max_length=500, blank=True, null=True, verbose_name="说明")
    type = models.CharField(max_length=10, blank=True, null=True, verbose_name="类型")
    status = models.BooleanField(default=False, verbose_name='状态')

    def __unicode__(self):
        return self.id

    class Meta:
        verbose_name = "dictionary表"
        verbose_name_plural = "dictionary表"
        db_table = 'dictionary'


class dds_data(models.Model):
    """
          dds_data_record table
        """
    id = models.AutoField(primary_key=True)
    hostID = models.CharField(max_length=30, blank=True, null=True, verbose_name="hostID")
    patientID = models.CharField(max_length=30, blank=True, null=True, verbose_name="patientID")
    accesionNumber = models.CharField(max_length=30, blank=True, null=True, verbose_name="accessionNumber")
    studyInstanceUID = models.CharField(max_length=30, blank=True, null=True, verbose_name="studyInstanceUID")
    pacsImageCount = models.IntegerField(blank=True, null=True, verbose_name="pacsImageCount")
    pacsImageInsertionTime = models.DateTimeField(auto_now=False, auto_now_add=True,
                                                  verbose_name="pacsImageInsertionTime")
    orthancImageCount = models.IntegerField(blank=True, null=True, verbose_name="orthancImageCount")
    orthancImageInsertionTime = models.DateTimeField(auto_now=False, auto_now_add=False,
                                                     verbose_name="orthancImageInsertionTime")
    orthancImageLastBuildTime = models.DateTimeField(auto_now=False, auto_now_add=False,
                                                     verbose_name="orthancImageLastBuildTime")

    def __unicode__(self):
        return self.id

    class Meta:
        verbose_name = "dds_data_record"
        verbose_name_plural = "dds_data_record"
        db_table = 'DDS_data'


class uploadfile(models.Model):
    """
          上传文件信息表 table
        """
    id = models.AutoField(primary_key=True)
    filename = models.CharField(max_length=30, blank=True, null=True, verbose_name="文件名")
    fileurl = models.CharField(max_length=300, blank=True, null=True, verbose_name="文件路径")
    fileid = models.IntegerField(blank=True, null=True, verbose_name="关联文件id")
    type = models.CharField(max_length=30, blank=True, null=True, verbose_name="类型")
    size = models.CharField(max_length=30, blank=True, null=True, verbose_name="文件大小")
    status = models.BooleanField(default=False, verbose_name='状态')
    remark = models.CharField(max_length=50, blank=True, null=True, verbose_name="备注")
    update_time = models.DateTimeField(auto_now=True, auto_now_add=False, verbose_name="修改时间")
    create_time = models.DateTimeField(auto_now=False, auto_now_add=True, verbose_name="创建时间")

    def __unicode__(self):
        return self.id

    class Meta:
        verbose_name = "uploadfile"
        verbose_name_plural = "uploadfile"
        db_table = 'uploadfile'


class install(models.Model):
    """
          部署安装信息表
        """
    id = models.AutoField(primary_key=True)
    server = models.CharField(max_length=30, blank=True, null=True, verbose_name="服务地址")
    testcase = models.CharField(max_length=30, blank=True, null=True, verbose_name="测试数据")
    version = models.CharField(max_length=30, blank=True, null=True, verbose_name="部署版本")
    starttime = models.CharField(max_length=30, blank=True, null=True, verbose_name="部署时间")
    Host = models.ForeignKey(Server, null=True, on_delete=models.CASCADE, verbose_name='Host')
    smokeid = models.IntegerField(blank=True, null=True, verbose_name='smoke_id')
    uid = models.IntegerField(blank=True, null=True, verbose_name="UIuid")
    type = models.CharField(max_length=30, blank=True, null=True, verbose_name="类型")
    crontab = models.CharField(max_length=30, blank=True, null=True, verbose_name="类型")
    status = models.BooleanField(default=False, verbose_name='状态')
    installstatus = models.BooleanField(default=False, verbose_name='部署状态 0升级安装 1全新安装')

    def __unicode__(self):
        return self.id

    @property
    def pwd(self):
        return Server.pwd

    class Meta:
        verbose_name = "install"
        verbose_name_plural = "install"
        db_table = 'install'


class message_group(models.Model):
    """
          信息组
        """
    id = models.AutoField(primary_key=True)
    party = models.CharField(max_length=30, blank=True, null=True, verbose_name="组")
    user = models.CharField(max_length=200, blank=True, null=True, verbose_name="人员")
    content = models.CharField(max_length=500, blank=True, null=True, verbose_name="内容")
    send_url = models.CharField(max_length=200, blank=True, null=True, verbose_name="发送组链接")
    mentioned_list = models.CharField(max_length=200, blank=True, null=True, verbose_name="@人员")
    mentioned_mobile_list = models.CharField(max_length=200, blank=True, null=True, verbose_name="@人员")
    type = models.CharField(max_length=20, blank=True, null=True, verbose_name="组")
    msgtype = models.CharField(max_length=20, blank=True, null=True, verbose_name="消息类型")
    status = models.BooleanField(default=False, verbose_name='状态')

    def __unicode__(self):
        return self.id

    class Meta:
        verbose_name = "message_group"
        verbose_name_plural = "message_group"
        db_table = 'message_group'


class message_detail(models.Model):
    """
          信息组
        """
    id = models.AutoField(primary_key=True)
    content = models.TextField(max_length=5000, blank=True, null=True, verbose_name="内容")
    msgtype = models.CharField(max_length=20, blank=True, null=True, verbose_name="类型")
    message = models.ForeignKey(message_group, null=True, on_delete=models.CASCADE, verbose_name='message')
    status = models.BooleanField(default=False, verbose_name='状态')

    def __unicode__(self):
        return self.id

    class Meta:
        verbose_name = "message_detail"
        verbose_name_plural = "message_detail"
        db_table = 'message_detail'


class build_package(models.Model):
    """
          部署打包信息表
        """
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30, blank=True, null=True, verbose_name="构建名称")
    service = models.CharField(max_length=30, blank=True, null=True, verbose_name="服务单元")
    code = models.CharField(max_length=50, blank=True, null=True, verbose_name="代码库")
    branch = models.CharField(max_length=30, blank=True, null=True, verbose_name="分支")
    type = models.CharField(max_length=30, blank=True, null=True, verbose_name="类型")
    crontab = models.CharField(max_length=30, blank=True, null=True, verbose_name="定时")
    packStatus = models.IntegerField(default=False, verbose_name='打包状态 0 checkout 1 build ')
    Host = models.ForeignKey(Server, null=True, on_delete=models.CASCADE, verbose_name='Host')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户')
    rely = models.BooleanField(default=False, verbose_name='依赖状态')
    status = models.BooleanField(default=False, verbose_name='状态')
    Project = models.ForeignKey(Project, null=True, on_delete=models.CASCADE, verbose_name='Project')
    update_time = models.DateTimeField(auto_now=True, auto_now_add=False, verbose_name="修改时间")
    create_time = models.DateTimeField(auto_now=False, auto_now_add=True, verbose_name="创建时间")

    def __unicode__(self):
        return self.id

    @property
    def pwd(self):
        return Server.pwd

    class Meta:
        verbose_name = "build_package"
        verbose_name_plural = "build_package"
        db_table = 'build_package'


class build_package_detail(models.Model):
    """
          部署打包信息表
        """
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30, blank=True, null=True, verbose_name="构建名称")
    service = models.CharField(max_length=30, blank=True, null=True, verbose_name="服务单元")
    code = models.CharField(max_length=50, blank=True, null=True, verbose_name="代码库")
    branch = models.CharField(max_length=30, blank=True, null=True, verbose_name="分支")
    type = models.CharField(max_length=30, blank=True, null=True, verbose_name="类型")
    crontab = models.CharField(max_length=30, blank=True, null=True, verbose_name="定时")
    packStatus = models.IntegerField(default=False, verbose_name='部署状态 0升级安装 1全新安装')
    Host = models.ForeignKey(Server, null=True, on_delete=models.CASCADE, verbose_name='Host')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户')
    rely = models.BooleanField(default=False, verbose_name='依赖状态')
    status = models.BooleanField(default=False, verbose_name='状态')
    Project = models.ForeignKey(Project, null=True, on_delete=models.CASCADE, verbose_name='Project')
    update_time = models.DateTimeField(auto_now=True, auto_now_add=False, verbose_name="修改时间")
    create_time = models.DateTimeField(auto_now=False, auto_now_add=True, verbose_name="创建时间")

    def __unicode__(self):
        return self.id

    class Meta:
        verbose_name = "build_package_detail"
        verbose_name_plural = "build_package_detail"
        db_table = 'build_package_detail'


class project_git(models.Model):
    """
          项目git 仓库存储
        """
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, blank=True, null=True, verbose_name="项目名称")
    gitname = models.CharField(max_length=80, blank=True, null=True, verbose_name="仓库名")
    code = models.CharField(max_length=100, blank=True, null=True, verbose_name="代码库")
    jenkins = models.CharField(max_length=50, blank=True, null=True, verbose_name="jenkins")
    Project = models.ForeignKey(Project, null=True, on_delete=models.CASCADE, verbose_name='Project')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户')
    status = models.BooleanField(default=False, verbose_name='状态')
    update_time = models.DateTimeField(auto_now=True, auto_now_add=False, verbose_name="修改时间")
    create_time = models.DateTimeField(auto_now=False, auto_now_add=True, verbose_name="创建时间")

    def __unicode__(self):
        return self.id

    class Meta:
        verbose_name = "project_git"
        verbose_name_plural = "project_git"
        db_table = 'project_git'
