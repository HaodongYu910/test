from django.db import models
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
    api_date = models.DateTimeField(auto_now=False, auto_now_add=False, null=True, blank=True, verbose_name="接口提测时间")
    app_date = models.DateTimeField(auto_now=False, auto_now_add=False, null=True, blank=True, verbose_name="app提测时间")
    api_online_date = models.DateTimeField(auto_now=False, auto_now_add=False, null=True, blank=True,
                                           verbose_name="接口上线时间")
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
        ('开发人员', '开发人员'),
        ('测试人员', '测试人员')
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


class GlobalHost(models.Model):
    """
    host域名
    """
    id = models.AutoField(primary_key=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name='项目')
    name = models.CharField(max_length=50, verbose_name='名称')
    host = models.CharField(max_length=50, verbose_name='Host地址')
    port = models.CharField(max_length=10, verbose_name='port')
    protocol = models.CharField(max_length=10,blank = True, null = True, verbose_name='协议')
    description = models.CharField(max_length=1024, blank=True, null=True, verbose_name='描述')
    status = models.BooleanField(default=True, verbose_name='状态')

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'HOST'
        verbose_name_plural = 'HOST管理'
        db_table = 'GlobalHost'


class CustomMethod(models.Model):
    """
    自定义方法
    """
    id = models.AutoField(primary_key=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name='项目')
    name = models.CharField(max_length=50, verbose_name='方法名')
    description = models.CharField(max_length=1024, blank=True, null=True, verbose_name='描述')
    type = models.CharField(max_length=50, verbose_name='类型')
    dataCode = models.TextField(verbose_name='代码')
    status = models.BooleanField(default=True, verbose_name='状态')

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = '自定义方法'
        verbose_name_plural = '自定义方法'
        db_table = 'CustomMethod'


class ApiGroupLevelFirst(models.Model):
    """
    接口一级分组
    """
    id = models.AutoField(primary_key=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name='项目')
    name = models.CharField(max_length=50, verbose_name='接口一级分组名称')

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '接口分组'
        verbose_name_plural = '接口分组'
        db_table = 'ApiGroupLevelFirst'


class ApiInfo(models.Model):
    """
    接口信息
    """
    id = models.AutoField(primary_key=True)
    project = models.ForeignKey(Project, related_name='api_project', on_delete=models.CASCADE, verbose_name='所属项目')
    apiGroupLevelFirst = models.ForeignKey(ApiGroupLevelFirst, blank=True, null=True,
                                           related_name='First',
                                           on_delete=models.SET_NULL, verbose_name='所属一级分组')
    name = models.CharField(max_length=50, verbose_name='接口名称')
    httpType = models.CharField(max_length=50, default='HTTP', verbose_name='http/https', choices=HTTP_CHOICE)
    requestType = models.CharField(max_length=50, verbose_name='请求方式', choices=REQUEST_TYPE_CHOICE)
    apiAddress = models.CharField(max_length=1024, verbose_name='接口地址')
    requestParameterType = models.CharField(max_length=50, verbose_name='请求参数格式', choices=REQUEST_PARAMETER_TYPE_CHOICE)
    status = models.BooleanField(default=True, verbose_name='状态')
    mockStatus = models.BooleanField(default=False, verbose_name="mock状态")
    mockCode = models.CharField(max_length=50, blank=True, null=True, verbose_name='HTTP状态', choices=HTTP_CODE_CHOICE)
    data = models.TextField(blank=True, null=True, verbose_name='mock内容')
    lastUpdateTime = models.DateTimeField(auto_now=True, verbose_name='最近更新')
    userUpdate = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, max_length=50, verbose_name='更新人',
                                   related_name='ApiUpdateUser')
    description = models.CharField(max_length=1024, blank=True, null=True, verbose_name='描述')

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '接口'
        verbose_name_plural = '接口管理'
        db_table = 'ApiInfo'


class ApiHead(models.Model):
    id = models.AutoField(primary_key=True)
    api = models.ForeignKey(ApiInfo, on_delete=models.CASCADE, verbose_name="所属接口", related_name='headers')
    name = models.CharField(max_length=1024, verbose_name="标签")
    value = models.CharField(max_length=1024, blank=True, null=True, verbose_name='内容')

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '请求头'
        verbose_name_plural = '请求头管理'
        db_table = 'ApiHead'


class ApiParameter(models.Model):
    id = models.AutoField(primary_key=True)
    api = models.ForeignKey(ApiInfo, on_delete=models.CASCADE, verbose_name="所属接口", related_name='requestParameter')
    name = models.CharField(max_length=1024, verbose_name="参数名")
    _type = models.CharField(default="String", max_length=1024, verbose_name='参数类型',
                             choices=(('Int', 'Int'), ('String', 'String')))
    value = models.CharField(max_length=1024, blank=True, null=True, verbose_name='参数值')
    required = models.BooleanField(default=True, verbose_name="是否必填")
    restrict = models.CharField(max_length=1024, blank=True, null=True, verbose_name="输入限制")
    description = models.CharField(max_length=1024, blank=True, null=True, verbose_name="描述")

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '请求参数'
        verbose_name_plural = '请求参数管理'
        db_table = 'ApiParameter'


class ApiParameterRaw(models.Model):
    id = models.AutoField(primary_key=True)
    api = models.OneToOneField(ApiInfo, on_delete=models.CASCADE, verbose_name="所属接口",
                               related_name='requestParameterRaw')
    data = models.TextField(blank=True, null=True, verbose_name='内容')

    class Meta:
        verbose_name = '请求参数Raw'
        db_table = 'ApiParameterRaw'


class ApiResponse(models.Model):
    id = models.AutoField(primary_key=True)
    api = models.ForeignKey(ApiInfo, on_delete=models.CASCADE, verbose_name="所属接口", related_name='response')
    name = models.CharField(max_length=1024, verbose_name="参数名")
    _type = models.CharField(default="String", max_length=1024, verbose_name='参数类型',
                             choices=(('Int', 'Int'), ('String', 'String')))
    value = models.CharField(max_length=1024, blank=True, null=True, verbose_name='参数值')
    required = models.BooleanField(default=True, verbose_name="是否必含")
    description = models.CharField(max_length=1024, blank=True, null=True, verbose_name="描述")

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '返回参数'
        verbose_name_plural = '返回参数管理'
        db_table = 'ApiResponse'


class APIRequestHistory(models.Model):
    """
    接口请求历史
    """
    id = models.AutoField(primary_key=True)
    api = models.ForeignKey(ApiInfo, on_delete=models.CASCADE, verbose_name='接口')
    requestTime = models.DateTimeField(auto_now_add=True, verbose_name='请求时间')
    requestType = models.CharField(max_length=50, verbose_name='请求方法')
    requestAddress = models.CharField(max_length=1024, verbose_name='请求地址')
    httpCode = models.CharField(max_length=50, verbose_name='HTTP状态')

    def __unicode__(self):
        return self.requestAddress

    class Meta:
        verbose_name = '接口请求历史'
        verbose_name_plural = '接口请求历史'
        db_table = 'APIRequestHistory'


class ApiOperationHistory(models.Model):
    """
    API操作历史
    """
    id = models.AutoField(primary_key=True)
    api = models.ForeignKey(ApiInfo, on_delete=models.CASCADE, verbose_name='接口')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, max_length=50, verbose_name='用户姓名')
    time = models.DateTimeField(auto_now_add=True, verbose_name='操作时间')
    description = models.CharField(max_length=1024, blank=True, null=True, verbose_name='操作内容')

    def __unicode__(self):
        return self.description

    class Meta:
        verbose_name = '接口操作历史'
        verbose_name_plural = '接口操作历史'
        db_table = 'ApiOperationHistory'


class AutomationGroupLevelFirst(models.Model):
    """
    自动化用例一级分组
    """
    id = models.AutoField(primary_key=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name='项目')
    name = models.CharField(max_length=50, verbose_name='用例一级分组')

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '用例分组'
        verbose_name_plural = '用例分组管理'
        db_table = 'AutomationGroupLevelFirst'


class AutomationTestCase(models.Model):
    """
    自动化测试用例
    """
    id = models.AutoField(primary_key=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name='所属项目')
    automationGroupLevelFirst = models.ForeignKey(AutomationGroupLevelFirst, blank=True, null=True,
                                                  on_delete=models.SET_NULL, verbose_name='所属用例一级分组',
                                                  related_name="automationGroup")
    # automationGroupLevelSecond = models.ForeignKey(AutomationGroupLevelSecond, blank=True, null=True,
    #                                                on_delete=models.SET_NULL, verbose_name='所属用例二级分组')
    caseName = models.CharField(max_length=50, verbose_name='用例名称')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="创建人",
                             related_name="createUser")
    description = models.CharField(max_length=1024, blank=True, null=True, verbose_name='描述')
    updateTime = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    def __unicode__(self):
        return self.caseName

    def __str__(self):
        return self.caseName

    class Meta:
        verbose_name = '自动化测试用例'
        verbose_name_plural = '自动化测试用例'
        db_table = 'AutomationTestCase'


class AutomationCaseApi(models.Model):
    """
    用例执行接口
    """
    id = models.AutoField(primary_key=True)
    automationTestCase = models.ForeignKey(AutomationTestCase, on_delete=models.CASCADE,
                                           verbose_name='用例', related_name="api")
    name = models.CharField(max_length=50, verbose_name='接口名称')
    httpType = models.CharField(max_length=50, default='HTTP', verbose_name='HTTP/HTTPS', choices=HTTP_CHOICE)
    requestType = models.CharField(max_length=50, verbose_name='请求方式', choices=REQUEST_TYPE_CHOICE)
    apiAddress = models.CharField(max_length=1024, verbose_name='接口地址')
    requestParameterType = models.CharField(max_length=50, verbose_name='参数请求格式', choices=REQUEST_PARAMETER_TYPE_CHOICE)
    formatRaw = models.BooleanField(default=False, verbose_name="是否转换成源数据")
    examineType = models.CharField(default='no_check', max_length=50, verbose_name='校验方式', choices=EXAMINE_TYPE_CHOICE)
    httpCode = models.CharField(max_length=50, blank=True, null=True, verbose_name='HTTP状态', choices=HTTP_CODE_CHOICE)
    responseData = models.TextField(blank=True, null=True, verbose_name='返回内容')

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '用例接口'
        verbose_name_plural = '用例接口管理'
        db_table = 'AutomationCaseApi'


class AutomationHead(models.Model):
    """
    请求头
    """
    id = models.AutoField(primary_key=True)
    automationCaseApi = models.ForeignKey(AutomationCaseApi, related_name='header',
                                          on_delete=models.CASCADE, verbose_name='接口')
    name = models.CharField(max_length=1024, verbose_name='参数名')
    value = models.CharField(max_length=1024, verbose_name='内容')
    interrelate = models.BooleanField(default=False, verbose_name='是否关联')

    def __unicode__(self):
        return self.value

    class Meta:
        verbose_name = '请求头'
        verbose_name_plural = '请求头管理'
        db_table = 'AutomationHead'


class AutomationParameter(models.Model):
    """
    请求的参数
    """
    id = models.AutoField(primary_key=True)
    automationCaseApi = models.ForeignKey(AutomationCaseApi, related_name='parameterList',
                                          on_delete=models.CASCADE, verbose_name='接口')
    name = models.CharField(max_length=1024, verbose_name='参数名')
    value = models.CharField(max_length=1024, verbose_name='内容', blank=True, null=True)
    interrelate = models.BooleanField(default=False, verbose_name='是否关联')

    def __unicode__(self):
        return self.value

    class Meta:
        verbose_name = '接口参数'
        verbose_name_plural = '接口参数管理'
        db_table = 'AutomationParameter'


class AutomationParameterRaw(models.Model):
    """
    请求的源数据参数
    """
    id = models.AutoField(primary_key=True)
    automationCaseApi = models.OneToOneField(AutomationCaseApi, related_name='parameterRaw',
                                             on_delete=models.CASCADE, verbose_name='接口')
    data = models.TextField(verbose_name='源数据请求参数', blank=True, null=True)

    class Meta:
        verbose_name = '源数据参数'
        verbose_name_plural = '源数据参数管理'
        db_table = 'AutomationParameterRaw'


class AutomationResponseJson(models.Model):
    """
    返回JSON参数
    """
    id = models.AutoField(primary_key=True)
    automationCaseApi = models.ForeignKey(AutomationCaseApi, related_name='response',
                                          on_delete=models.CASCADE, verbose_name='接口')
    name = models.CharField(max_length=1024, verbose_name='JSON参数', blank=True, null=True)
    tier = models.CharField(max_length=1024, verbose_name='层级关系', blank=True, null=True)
    type = models.CharField(max_length=1024, verbose_name="关联类型", default="json",
                            choices=(('json', 'json'), ('Regular', 'Regular')))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '结果JSON参数'
        verbose_name_plural = '结果JSON参数管理'
        db_table = 'AutomationResponseJson'


class AutomationTestResult(models.Model):
    """
    手动执行结果
    """
    id = models.AutoField(primary_key=True)
    automationCaseApi = models.OneToOneField(AutomationCaseApi, on_delete=models.CASCADE, verbose_name='接口'
                                             , related_name="test_result")
    url = models.CharField(max_length=1024, verbose_name='请求地址')
    requestType = models.CharField(max_length=1024, verbose_name='请求方式', choices=REQUEST_TYPE_CHOICE)
    host = models.CharField(max_length=1024, verbose_name='测试地址', null=True, blank=True)
    header = models.CharField(max_length=1024, blank=True, null=True, verbose_name='请求头')
    parameter = models.TextField(blank=True, null=True, verbose_name='请求参数')
    statusCode = models.CharField(blank=True, null=True, max_length=1024, verbose_name='期望HTTP状态',
                                  choices=HTTP_CODE_CHOICE)
    examineType = models.CharField(max_length=1024, verbose_name='匹配规则')
    data = models.TextField(blank=True, null=True, verbose_name='规则内容')
    result = models.CharField(max_length=50, verbose_name='测试结果', choices=RESULT_CHOICE)
    httpStatus = models.CharField(max_length=50, blank=True, null=True, verbose_name='http状态', choices=HTTP_CODE_CHOICE)
    responseData = models.TextField(blank=True, null=True, verbose_name='实际返回内容')
    testTime = models.DateTimeField(auto_now_add=True, verbose_name='测试时间')

    def __unicode__(self):
        return self.httpStatus

    class Meta:
        verbose_name = '手动测试结果'
        verbose_name_plural = '手动测试结果管理'
        db_table = 'AutomationTestResult'


class AutomationTestTask(models.Model):
    """
    用例定时任务
    """
    id = models.AutoField(primary_key=True)
    project = models.OneToOneField(Project, on_delete=models.CASCADE, verbose_name='项目')
    Host = models.ForeignKey(GlobalHost, on_delete=models.CASCADE, verbose_name='HOST')
    name = models.CharField(max_length=50, verbose_name='任务名称')
    type = models.CharField(max_length=50, verbose_name='类型', choices=TASK_CHOICE)
    frequency = models.IntegerField(blank=True, null=True, verbose_name='间隔')
    unit = models.CharField(max_length=50, blank=True, null=True, verbose_name='单位', choices=UNIT_CHOICE)
    startTime = models.DateTimeField(max_length=50, verbose_name='开始时间')
    endTime = models.DateTimeField(max_length=50, verbose_name='结束时间')

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '用例定时任务'
        verbose_name_plural = '用例定时任务管理'
        db_table = 'AutomationTestTask'


class AutomationTaskRunTime(models.Model):
    """
    用例执行开始和结束时间
    """
    id = models.AutoField(primary_key=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name='项目')
    startTime = models.CharField(max_length=50, verbose_name='开始时间')
    host = models.CharField(max_length=1024, null=True, blank=True, verbose_name='测试地址')
    elapsedTime = models.CharField(max_length=50, verbose_name='结束时间')

    class Meta:
        verbose_name = '用例任务执行时间'
        verbose_name_plural = '用例任务执行时间'
        db_table = 'AutomationTaskRunTime'


class AutomationCaseTestResult(models.Model):
    """
    任务执行结果
    """
    id = models.AutoField(primary_key=True)
    automationCaseApi = models.ForeignKey(AutomationCaseApi, on_delete=models.CASCADE, verbose_name='接口'
                                          , related_name="auto_result")
    header = models.CharField(max_length=1024, blank=True, null=True, verbose_name='请求头')
    parameter = models.TextField(blank=True, null=True, verbose_name='请求参数')
    result = models.CharField(max_length=50, verbose_name='测试结果', choices=RESULT_CHOICE)
    httpStatus = models.CharField(max_length=50, blank=True, null=True, verbose_name='http状态', choices=HTTP_CODE_CHOICE)
    responseHeader = models.TextField(blank=True, null=True, verbose_name='返回头')
    responseData = models.TextField(blank=True, null=True, verbose_name='实际返回内容')
    testTime = models.CharField(max_length=128, null=True, blank=True, verbose_name='测试时间')

    def __unicode__(self):
        return self.httpStatus

    class Meta:
        verbose_name = '自动测试结果'
        verbose_name_plural = '自动测试结果管理'
        db_table = 'AutomationCaseTestResult'


class AutomationReportSendConfig(models.Model):
    """
    报告发送人配置
    """
    id = models.AutoField(primary_key=True)
    project = models.OneToOneField(Project, on_delete=models.CASCADE, verbose_name="项目")
    reportFrom = models.EmailField(max_length=1024, blank=True, null=True, verbose_name="发送人邮箱")
    mailUser = models.CharField(max_length=1024, blank=True, null=True, verbose_name="用户名")
    mailPass = models.CharField(max_length=1024, blank=True, null=True, verbose_name="口令")
    mailSmtp = models.CharField(max_length=1024, blank=True, null=True, verbose_name="邮箱服务器")

    def __unicode__(self):
        return self.reportFrom

    class Meta:
        verbose_name = "邮件发送配置"
        verbose_name_plural = "邮件发送配置"
        db_table = 'AutomationReportSendConfig'


class VisitorsRecord(models.Model):
    """
    访客记录
    """
    id = models.AutoField(primary_key=True)
    formattedAddress = models.CharField(max_length=1024, blank=True, null=True, verbose_name="访客地址")
    country = models.CharField(max_length=50, blank=True, null=True, verbose_name="国家")
    province = models.CharField(max_length=50, blank=True, null=True, verbose_name="省份")
    city = models.CharField(max_length=50, blank=True, null=True, verbose_name="城市")
    district = models.CharField(max_length=50, blank=True, null=True, verbose_name="县级")
    township = models.CharField(max_length=50, blank=True, null=True, verbose_name="镇")
    street = models.CharField(max_length=50, blank=True, null=True, verbose_name="街道")
    number = models.CharField(max_length=50, blank=True, null=True, verbose_name="门牌号")
    success = models.CharField(max_length=50, blank=True, null=True, verbose_name="成功")
    reason = models.CharField(max_length=1024, blank=True, null=True, verbose_name="原因")
    callTime = models.DateTimeField(auto_now_add=True, verbose_name="访问时间")

    def __unicode__(self):
        return self.formattedAddress

    class Meta:
        verbose_name = "访客"
        verbose_name_plural = "访客查看"
        db_table = 'VisitorsRecord'


# Create your models here.
class test_report(models.Model):
    """
      邮件
    """
    report_id = models.AutoField(primary_key=True)
    test_version = models.CharField(max_length=10, blank=True, null=True, verbose_name="Boimind版本")
    cns_version = models.CharField(max_length=10, blank=True, null=True, verbose_name="CoinNess版本")
    type = models.IntegerField(blank=True, null=True, verbose_name="类型（1.每日报告 2.测试报告 3.质量报告）")
    send_time = models.CharField(max_length=5, blank=True, null=True, verbose_name="发送时间")
    title = models.CharField(max_length=20, blank=True, null=True, verbose_name="邮件标题")
    receiver = models.CharField(max_length=500, blank=True, null=True, verbose_name="发送人员")
    email_cc = models.CharField(max_length=200, blank=True, null=True, verbose_name="抄送人员")
    content_id = models.CharField(max_length=20, blank=True, null=True, verbose_name="内容id")
    update_time = models.DateTimeField(auto_now=True, auto_now_add=False, verbose_name="修改时间")
    create_time = models.DateTimeField(auto_now=False, auto_now_add=True, verbose_name="创建时间")

    def __unicode__(self):
        return self.receiver

    class Meta:
        verbose_name = "邮件报告"
        verbose_name_plural = "邮件报告"
        db_table = 'test_report'


class test_content(models.Model):
    """
      邮件内容
    """
    content_id = models.AutoField(primary_key=True)
    project_content = models.CharField(max_length=1000, blank=True, null=True, verbose_name="项目内容")
    product_content = models.CharField(max_length=1000, blank=True, null=True, verbose_name="需求内容")
    case_content = models.CharField(max_length=1000, blank=True, null=True, verbose_name="case 内容")
    bug_content = models.CharField(max_length=500, blank=True, null=True, verbose_name="bug 内容")
    performance_content = models.CharField(max_length=1000, blank=True, null=True, verbose_name="性能内容")
    report_id = models.IntegerField(blank=True, null=True, verbose_name="邮件id")
    update_time = models.DateTimeField(auto_now=True, auto_now_add=False, verbose_name="修改时间")
    create_time = models.DateTimeField(auto_now=False, auto_now_add=True, verbose_name="创建时间")

    # report_id = models.ForeignKey(test_report, on_delete=models.CASCADE, related_name='report_id')

    def __unicode__(self):
        return self.receiver

    class Meta:
        verbose_name = "邮件内容"
        verbose_name_plural = "邮件内容"
        db_table = 'test_content'


class test_risk(models.Model):
    """
      测试风险点
    """
    risk_id = models.AutoField(primary_key=True)
    project_id = models.CharField(max_length=10, blank=True, null=True, verbose_name="项目ID")
    risk = models.CharField(max_length=100, blank=True, null=True, verbose_name="风险内容")
    development = models.CharField(max_length=20, blank=True, null=True, verbose_name="开发人员")
    delay = models.CharField(max_length=4, blank=True, null=True, verbose_name="延期日期")
    solution_status = models.CharField(max_length=1, blank=True, null=True, verbose_name="解决状态  0是未解决，1是解决")
    status = models.CharField(max_length=1, blank=True, null=True, verbose_name="0是显示，1是不显示")
    update_time = models.DateTimeField(auto_now=True, auto_now_add=False, verbose_name="修改时间")
    create_time = models.DateTimeField(auto_now=False, auto_now_add=True, verbose_name="创建时间")

    def __unicode__(self):
        return self.risk

    class Meta:
        verbose_name = "测试风险点"
        verbose_name_plural = "测试风险点"
        db_table = 'test_risk'


class base_data(models.Model):
    """
      基础数据表
    """
    id = models.AutoField(primary_key=True)
    content = models.CharField(max_length=500, blank=True, null=True, verbose_name="内容")
    type = models.CharField(max_length=10, blank=True, null=True, verbose_name="类型")
    select_type = models.CharField(max_length=20, blank=True, null=True, verbose_name="查询类型")
    remarks = models.CharField(max_length=100, blank=True, null=True, verbose_name="备注")
    other = models.CharField(max_length=10, blank=True, null=True, verbose_name="其他")
    predictor = models.CharField(max_length=25, blank=True, null=True, verbose_name="其他")
    status = models.BooleanField(default=True, verbose_name="0是关闭，1是启用")
    update_time = models.DateTimeField(auto_now=True, auto_now_add=False, verbose_name="修改时间")
    create_time = models.DateTimeField(auto_now=False, auto_now_add=True, verbose_name="创建时间")

    def __unicode__(self):
        return self.select_type

    class Meta:
        verbose_name = "基础数据表"
        verbose_name_plural = "基础数据表"
        db_table = 'base_data'


class stress(models.Model):
    """
      性能测试记录表
    """
    id = models.AutoField(primary_key=True)
    projectname = models.CharField(max_length=20, blank=True, null=True, verbose_name="项目名称")
    version = models.CharField(max_length=20, blank=True, null=True, verbose_name="测试版本")
    loadserver = models.CharField(max_length=40, blank=True, null=True, verbose_name="测试环境")
    testdata = models.CharField(max_length=400, blank=True, null=True, verbose_name="测试数据")
    thread = models.CharField(max_length=4, blank=True, null=True, verbose_name="线程数")
    synchroniz = models.CharField(max_length=4, blank=True, null=True, verbose_name="并发vu")
    ramp = models.CharField(max_length=4, blank=True, null=True, verbose_name="ramp up time")
    loop_count = models.CharField(max_length=4, blank=True, null=True, verbose_name="循环次数")
    duration = models.CharField(max_length=4, blank=True, null=True, verbose_name="持续时间")
    start_delay = models.CharField(max_length=4, blank=True, null=True, verbose_name="启动延时 秒")
    dicom_send = models.CharField(max_length=4, blank=True, null=True, verbose_name="duration 发送")
    start_date = models.CharField(max_length=20, blank=True, null=True, verbose_name="压测开始时间")
    end_date = models.CharField(max_length=20, blank=True, null=True, verbose_name="压测结束时间")
    loop_time = models.CharField(max_length=10, blank=True, null=True, verbose_name="执行时间")
    jmeterstatus = models.BooleanField(default=True, verbose_name='jmeter状态')
    status = models.BooleanField(default=True, verbose_name='状态')
    hostid = models.IntegerField(default=True, verbose_name='HOST id')
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
      性能测试数据表
    """
    id = models.AutoField(primary_key=True)
    stressid = models.CharField(max_length=5, blank=True, null=True, verbose_name="stress表ID")
    studyuid = models.CharField(max_length=200, blank=True, null=True, verbose_name="测试环境")
    imagecount = models.CharField(max_length=5, blank=True, null=True, verbose_name="张数")
    slicenumber = models.CharField(max_length=5, blank=True, null=True, verbose_name="层厚")
    diseases = models.CharField(max_length=10, blank=True, null=True, verbose_name="病种")
    graphql = models.CharField(max_length=500, blank=True, null=True, verbose_name="手动预测json")
    fileurl = models.CharField(max_length=200, blank=True, null=True, verbose_name=" 路径")
    benchmarkstatus = models.BooleanField(default=False, verbose_name='是否基准')
    status = models.BooleanField(default=False, verbose_name='状态')
    def __unicode__(self):
        return self.stressid

    class Meta:
        verbose_name = "性能测试数据表"
        verbose_name_plural = "性能测试数据表"
        db_table = 'stress_record'
class stress_job(models.Model):
    """
          压测job记录表
        """
    id = models.AutoField(primary_key=True)
    version = models.CharField(max_length=30, blank=True, null=True, verbose_name="版本")
    studyuid = models.CharField(max_length=200, blank=True, null=True, verbose_name="uid")
    type = models.CharField(max_length=20, blank=True, null=True, verbose_name="类型")
    job_id = models.CharField(max_length=80, blank=True, null=True, verbose_name="id")
    sec = models.CharField(max_length=20, blank=True, null=True, verbose_name="预测时间")
    start = models.CharField(max_length=30, blank=True, null=True, verbose_name="开始时间")
    end = models.CharField(max_length=30, blank=True, null=True, verbose_name="结束时间")
    modelname = models.CharField(max_length=30, blank=True, null=True, verbose_name="模型名称")
    images= models.CharField(max_length=30, blank=True, null=True, verbose_name="模型名称")
    stressid = models.IntegerField(blank=True, null=True, verbose_name="stressID")

    def __unicode__(self):
        return self.version

    class Meta:
        verbose_name = "压测结果记录表"
        verbose_name_plural = "压测结果记录表"
        db_table = 'stress_job'

class stress_result(models.Model):
    """
          压测结果记录表
        """
    id = models.AutoField(primary_key=True)
    version = models.CharField(max_length=10, blank=True, null=True, verbose_name="版本")
    modelname = models.CharField(max_length=30, blank=True, null=True, verbose_name="模型")
    type = models.CharField(max_length=15, blank=True, null=True, verbose_name="结果类型")
    slicenumber = models.CharField(max_length=6, blank=True, null=True, verbose_name="层厚")
    count = models.IntegerField( blank=True, null=True, verbose_name="次数")
    avg = models.CharField(max_length=10, blank=True, null=True, verbose_name="平均值")
    single = models.CharField(max_length=10, blank=True, null=True, verbose_name="单任务")
    median = models.CharField(max_length=10, blank=True, null=True, verbose_name="中间值")
    min = models.CharField(max_length=10, blank=True, null=True, verbose_name="最小时间")
    max = models.CharField(max_length=10, blank=True, null=True, verbose_name="最大时间")
    coef = models.CharField(max_length=10, blank=True, null=True, verbose_name="系数")
    rate = models.TextField(max_length=10, blank=True, null=True, verbose_name="预测成功率")
    minimages= models.TextField(max_length=10, blank=True, null=True, verbose_name="影像张数")
    maximages= models.TextField(max_length=10, blank=True, null=True, verbose_name="影像张数")
    avgimages= models.TextField(max_length=10, blank=True, null=True, verbose_name="影像张数")
    stressid = models.IntegerField(blank=True, null=True, verbose_name="stressID")
    update_time = models.DateTimeField(auto_now=True, auto_now_add=False, verbose_name="修改时间")
    create_time = models.DateTimeField(auto_now=False, auto_now_add=True, verbose_name="创建时间")

    def __unicode__(self):
        return self.version

    class Meta:
        verbose_name = "压测结果记录表"
        verbose_name_plural = "压测结果记录表"
        db_table = 'stress_result'

class duration_record(models.Model):
    """
          持续化测试记录表
        """
    id = models.AutoField(primary_key=True)
    patientid = models.CharField(max_length=80, blank=True, null=True, verbose_name="patientid")
    accessionnumber = models.CharField(max_length=80, blank=True, null=True, verbose_name="accessionnumber")
    studyinstanceuid = models.CharField(max_length=200, blank=True, null=True, verbose_name="数据uid")
    studyolduid = models.CharField(max_length=200, blank=True, null=True, verbose_name="影像张数验证")
    imagecount = models.CharField(max_length=50, blank=True, null=True, verbose_name="发送影像张数")
    imagecount_server = models.CharField(max_length=50, blank=True, null=True, verbose_name="接收影像张数")
    aistatus = models.CharField(max_length=10, blank=True, null=True, verbose_name="AI预测结果")
    diagnosis = models.CharField(max_length=200, blank=True, null=True, verbose_name="诊断结果")
    sendserver = models.CharField(max_length=20, blank=True, null=True, verbose_name="发送服务")
    sendtime = models.CharField(max_length=20, blank=True, null=True, verbose_name="发送开始时间")
    endtime = models.CharField(max_length=20, blank=True, null=True, verbose_name="发送结束时间")
    time = models.CharField(max_length=20, blank=True, null=True, verbose_name="发送时间")
    duration_id = models.CharField(max_length=20, blank=True, null=True, verbose_name="关联持续id")
    update_time = models.DateTimeField(auto_now=True, auto_now_add=False, verbose_name="修改时间")
    create_time = models.DateTimeField(auto_now=False, auto_now_add=True, verbose_name="创建时间")

    def __unicode__(self):
        return self.studyinstanceuid

    class Meta:
        verbose_name = "持续化测试记录表"
        verbose_name_plural = "持续化测试记录表"
        db_table = 'duration_record'

class duration(models.Model):
    """
          持续化测试记录表
        """
    id = models.AutoField(primary_key=True)
    server = models.CharField(max_length=20, blank=True, null=True, verbose_name="服务器ip")
    port = models.CharField(max_length=10, blank=True, null=True, verbose_name="服务器端口号")
    aet = models.CharField(max_length=20, blank=True, null=True, verbose_name="aet")
    keyword = models.CharField(max_length=30, blank=True, null=True, verbose_name="匿名名称")
    dicom = models.CharField(max_length=100, blank=True, null=True, verbose_name="dicom数据")
    sendcount = models.IntegerField(blank=True, null=True, verbose_name="共计发送")
    end_time = models.CharField(max_length=20, blank=True, null=True, verbose_name="结束时间")
    sleepcount = models.CharField(max_length=20, blank=True, null=True, verbose_name="睡眠张数")
    sleeptime = models.CharField(max_length=20, blank=True, null=True, verbose_name="睡眠时间")
    series = models.CharField(max_length=5, blank=True, null=True, verbose_name="series")
    sendstatus = models.BooleanField(default=True, verbose_name='发送状态')
    status = models.BooleanField(default=False, verbose_name='状态')
    dds = models.CharField(max_length=20, blank=True, null=True,  verbose_name='dds 服务')
    hostid = models.IntegerField(default=True, verbose_name='HOST id')
    update_time = models.DateTimeField(auto_now=True, auto_now_add=False, verbose_name="修改时间")
    create_time = models.DateTimeField(auto_now=False, auto_now_add=True, verbose_name="创建时间")

    def __unicode__(self):
        return self.server

    class Meta:
        verbose_name = "持续化配置"
        verbose_name_plural = "持续化配置"
        db_table = 'duration'


class dicom(models.Model):
    """
          测试数据表
        """
    id = models.AutoField(primary_key=True)
    patientid = models.CharField(max_length=50, blank=True, null=True, verbose_name="patientid")
    studyinstanceuid = models.CharField(max_length=120, blank=True, null=True, verbose_name="数据uid")
    diseases = models.CharField(max_length=20, blank=True, null=True, verbose_name="预测类型")
    slicenumber = models.CharField(max_length=6, blank=True, null=True, verbose_name="肺炎层厚")
    imagecount = models.CharField(max_length=5, blank=True, null=True, verbose_name="张数")
    vote = models.CharField(max_length=800, blank=True, null=True, verbose_name="挂载")
    fileid =  models.CharField(max_length=5, blank=True, null=True, verbose_name="文件ID")
    diagnosis = models.CharField(max_length=200, blank=True, null=True, verbose_name="诊断结果")
    server = models.CharField(max_length=20, blank=True, null=True, verbose_name="服务")
    type = models.CharField(max_length=10, blank=True, null=True, verbose_name="类型")
    route = models.CharField(max_length=100, blank=True, null=True, verbose_name="路径")
    update_time = models.DateTimeField(auto_now=True, auto_now_add=False, verbose_name="修改时间")
    create_time = models.DateTimeField(auto_now=False, auto_now_add=True, verbose_name="创建时间")

    def __unicode__(self):
        return self.studyinstanceuid

    class Meta:
        verbose_name = "dicom数据表"
        verbose_name_plural = "dicom数据表"
        db_table = 'dicom'

class smoke(models.Model):
    """
          smoke测试记录表
        """
    id = models.AutoField(primary_key=True)
    version = models.CharField(max_length=20, blank=True, null=True, verbose_name="版本")
    diseases = models.CharField(max_length=20, blank=True, null=True, verbose_name="病种")
    progress = models.CharField(max_length=5, blank=True, null=True, verbose_name="进度")
    thread = models.CharField(max_length=5, blank=True, null=True, verbose_name="线程数")
    starttime = models.CharField(max_length=20, blank=True, null=True, verbose_name="开始预测时间")
    completiontime = models.CharField(max_length=20, blank=True, null=True, verbose_name="结束预测时间")
    count = models.CharField(max_length=5, blank=True, null=True, verbose_name="count")
    hostid =models.IntegerField(default=False, verbose_name='hostid')
    status = models.BooleanField(default=False, verbose_name='状态')

    def __unicode__(self):
        return self.version

    class Meta:
        verbose_name = "smoke测试表"
        verbose_name_plural = "smoke测试表"
        db_table = 'smoke'

class dicom_record(models.Model):
    """
          测试记录表
        """
    id = models.AutoField(primary_key=True)
    version = models.CharField(max_length=10, blank=True, null=True, verbose_name="版本")
    patientid = models.CharField(max_length=30, blank=True, null=True, verbose_name="id")
    server = models.CharField(max_length=20, blank=True, null=True, verbose_name="服务")
    studyinstanceuid = models.CharField(max_length=150, blank=True, null=True, verbose_name="数据uid")
    diseases = models.CharField(max_length=20, blank=True, null=True, verbose_name="病种")
    slicenumber = models.CharField(max_length=20, blank=True, null=True, verbose_name="slicenumber")
    aistatus = models.CharField(max_length=5, blank=True, null=True, verbose_name="预测结果")
    aidiagnosis = models.CharField(max_length=100, blank=True, null=True, verbose_name="ai诊断结果")
    diagnosis = models.CharField(max_length=100, blank=True, null=True, verbose_name="诊断结果")
    starttime = models.CharField(max_length=20, blank=True, null=True, verbose_name="开始预测时间")
    completiontime = models.CharField(max_length=20, blank=True, null=True, verbose_name="结束预测时间")
    report = models.TextField(max_length=100, blank=True, null=True, verbose_name="诊断报告")
    type = models.TextField(max_length=10, blank=True, null=True, verbose_name="诊断报告")
    status = models.BooleanField(default=False, verbose_name='状态')
    hostid =models.IntegerField(default=False, verbose_name='hostid')
    update_time = models.DateTimeField(auto_now=True, auto_now_add=False, verbose_name="修改时间")
    create_time = models.DateTimeField(auto_now=False, auto_now_add=True, verbose_name="创建时间")

    def __unicode__(self):
        return self.version

    class Meta:
        verbose_name = "测试记录表"
        verbose_name_plural = "测试记录表"
        db_table = 'dicom_record'


class pid(models.Model):
    """
          pid表
        """
    id = models.AutoField(primary_key=True)
    pid = models.IntegerField(blank=True, null=True, verbose_name="进程号")
    durationid = models.CharField(max_length=5, blank=True, null=True, verbose_name="持续化id")


    def __unicode__(self):
        return self.pid

    class Meta:
        verbose_name = "pid表"
        verbose_name_plural = "pid表"
        db_table = 'pid'


class interface(models.Model):
    """
          Interface表
        """
    id = models.AutoField(primary_key=True)
    interfacename = models.CharField(max_length=50, blank=True, null=True, verbose_name="接口名")
    json = models.CharField(max_length=2500, blank=True, null=True, verbose_name="json")
    type = models.CharField(max_length=10, blank=True, null=True, verbose_name="类型")
    status = models.BooleanField(default=False, verbose_name='状态')


    def __unicode__(self):
        return self.id

    class Meta:
        verbose_name = "Interface表"
        verbose_name_plural = "Interface表"
        db_table = 'interface'

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


class dds_host(models.Model):
    """
    dicommaster host record model class. class name is not the database name, they can be different.
    """
    # attributes
    id = models.AutoField(primary_key=True)
    dds_ip = models.CharField(max_length=30, blank=True, null=True, verbose_name="dds_ip")

    def __unicode__(self):
        return self.version

    class Meta:
        verbose_name = "dicommaster_host_record"
        verbose_name_plural = "dicommaster_host_record"
        db_table = 'DDS_host'    #database name

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
    pacsImageInsertionTime = models.DateTimeField(auto_now=False, auto_now_add=True, verbose_name="pacsImageInsertionTime")
    orthancImageCount = models.IntegerField(blank=True, null=True, verbose_name="orthancImageCount")
    orthancImageInsertionTime = models.DateTimeField(auto_now=False, auto_now_add=False, verbose_name="orthancImageInsertionTime")
    orthancImageLastBuildTime = models.DateTimeField(auto_now=False, auto_now_add=False, verbose_name="orthancImageLastBuildTime")

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
    fileurl = models.CharField(max_length=30, blank=True, null=True, verbose_name="文件路径")
    fileid = models.IntegerField(blank=True, null=True, verbose_name="关联文件id")
    type = models.CharField(max_length=30, blank=True, null=True, verbose_name="类型")
    status = models.BooleanField(default=False, verbose_name='状态')
    update_time = models.DateTimeField(auto_now=True, auto_now_add=False, verbose_name="修改时间")
    create_time = models.DateTimeField(auto_now=False, auto_now_add=True, verbose_name="创建时间")

    def __unicode__(self):
        return self.id

    class Meta:
        verbose_name = "uploadfile"
        verbose_name_plural = "uploadfile"
        db_table = 'uploadfile'