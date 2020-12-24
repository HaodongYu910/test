#! /usr/bin/env python
# -*- coding: utf-8
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.authtoken.models import Token

from .models import *


class TokenSerializer(serializers.ModelSerializer):
    """
    用户信息序列化
    """
    first_name = serializers.CharField(source="user.first_name")
    last_name = serializers.CharField(source="user.last_name")
    phone = serializers.CharField(source="user.user.phone")
    email = serializers.CharField(source="user.email")
    date_joined = serializers.CharField(source="user.date_joined")

    class Meta:
        model = Token
        fields = ('first_name', 'last_name', 'phone', 'email', 'key', 'date_joined')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name')


class ProjectDeserializer(serializers.ModelSerializer):
    """
    项目信息反序列化
    """

    class Meta:
        model = Project
        fields = (
            'id', 'name', 'version', 'type', 'status', 'start_date', 'api_date', 'app_date', 'api_online_date',
            'end_date',
            'client', 'projectstatus', 'description', 'LastUpdateTime', 'createTime', 'user')


class ProjectSerializer(serializers.ModelSerializer):
    """
    项目信息序列化
    """
    apiCount = serializers.SerializerMethodField()
    dynamicCount = serializers.SerializerMethodField()
    memberCount = serializers.SerializerMethodField()
    LastUpdateTime = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    createTime = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    user = serializers.CharField(source='user.first_name')

    class Meta:
        model = Project
        fields = (
            'id', 'name', 'version', 'type', 'status', 'start_date', 'api_date', 'app_date', 'api_online_date',
            'end_date',
            'client', 'projectstatus', 'LastUpdateTime', 'createTime', 'apiCount',
            'dynamicCount', 'memberCount', 'description', 'user')

    def get_apiCount(self, obj):
        return obj.api_project.all().count()

    def get_dynamicCount(self, obj):
        return obj.dynamic_project.all().count()

    def get_memberCount(self, obj):
        return obj.member_project.all().count()


class ProjectDynamicDeserializer(serializers.ModelSerializer):
    """
    项目动态信息反序列化
    """

    class Meta:
        model = ProjectDynamic
        fields = ('id', 'project', 'time', 'type', 'operationObject', 'user', 'description')


class ProjectDynamicSerializer(serializers.ModelSerializer):
    """
    项目动态信息序列化
    """
    operationUser = serializers.CharField(source='user.first_name')
    time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)

    class Meta:
        model = ProjectDynamic
        fields = ('id', 'time', 'type', 'operationObject', 'operationUser', 'description')


class ProjectMemberDeserializer(serializers.ModelSerializer):
    """
    项目成员信息反序列化
    """

    class Meta:
        model = ProjectMember
        fields = ('id', 'permissionType', 'project', 'user')


class ProjectMemberSerializer(serializers.ModelSerializer):
    """
    项目成员信息序列化
    """
    username = serializers.CharField(source='user.first_name')
    userPhone = serializers.CharField(source='user.user.phone')
    userEmail = serializers.CharField(source='user.email')

    class Meta:
        model = ProjectMember
        fields = ('id', 'permissionType', 'username', 'userPhone', 'userEmail')


class GlobalHostSerializer(serializers.ModelSerializer):
    """
    host信息序列化
    """

    class Meta:
        model = GlobalHost
        fields = ('id', 'project_id', 'name', 'host','port', 'status', 'description')


class ApiGroupLevelFirstSerializer(serializers.ModelSerializer):
    """
    接口一级分组信息序列化
    """

    class Meta:
        model = ApiGroupLevelFirst
        fields = ('id', 'project_id', 'name')


class ApiGroupLevelFirstDeserializer(serializers.ModelSerializer):
    """
    接口一级分组信息反序列化
    """

    class Meta:
        model = ApiGroupLevelFirst
        fields = ('id', 'project_id', 'name')


class ApiHeadSerializer(serializers.ModelSerializer):
    """
    接口请求头序列化
    """

    class Meta:
        model = ApiHead
        fields = ('id', 'api', 'name', 'value')


class ApiHeadDeserializer(serializers.ModelSerializer):
    """
    接口请求头反序列化
    """

    class Meta:
        model = ApiHead
        fields = ('id', 'api', 'name', 'value')


class ApiParameterSerializer(serializers.ModelSerializer):
    """
    接口请求参数序列化
    """

    class Meta:
        model = ApiParameter
        fields = ('id', 'api', 'name', 'value', '_type', 'required', 'restrict', 'description')


class ApiParameterDeserializer(serializers.ModelSerializer):
    """
    接口请求参数反序列化
    """

    class Meta:
        model = ApiParameter
        fields = ('id', 'api', 'name', 'value', '_type', 'required', 'restrict', 'description')


class ApiParameterRawSerializer(serializers.ModelSerializer):
    """
    接口请求参数源数据序列化
    """

    class Meta:
        model = ApiParameterRaw
        fields = ('id', 'api', 'data')


class ApiParameterRawDeserializer(serializers.ModelSerializer):
    """
    接口请求参数源数据序列化
    """

    class Meta:
        model = ApiParameterRaw
        fields = ('id', 'api', 'data')


class ApiResponseSerializer(serializers.ModelSerializer):
    """
    接口返回参数序列化
    """

    class Meta:
        model = ApiResponse
        fields = ('id', 'api', 'name', 'value', '_type', 'required', 'description')


class ApiResponseDeserializer(serializers.ModelSerializer):
    """
    接口返回参数序列化
    """

    class Meta:
        model = ApiResponse
        fields = ('id', 'api', 'name', 'value', '_type', 'required', 'description')


class ApiInfoSerializer(serializers.ModelSerializer):
    """
    接口详细信息序列化
    """
    lastUpdateTime = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    headers = ApiHeadSerializer(many=True, read_only=True)
    requestParameter = ApiParameterSerializer(many=True, read_only=True)
    response = ApiResponseSerializer(many=True, read_only=True)
    requestParameterRaw = ApiParameterRawSerializer(many=False, read_only=True)
    userUpdate = serializers.CharField(source='userUpdate.first_name')

    class Meta:
        model = ApiInfo
        fields = ('id', 'apiGroupLevelFirst', 'name', 'httpType', 'requestType', 'apiAddress', 'headers',
                  'requestParameterType', 'requestParameter', 'requestParameterRaw', 'status',
                  'response', 'mockCode', 'data', 'lastUpdateTime', 'userUpdate', 'description')


class ApiInfoDeserializer(serializers.ModelSerializer):
    """
    接口详细信息序列化
    """

    class Meta:
        model = ApiInfo
        fields = ('id', 'project_id', 'name', 'httpType',
                  'requestType', 'apiAddress', 'requestParameterType', 'status',
                  'mockCode', 'data', 'lastUpdateTime', 'userUpdate', 'description')


class ApiInfoDocSerializer(serializers.ModelSerializer):
    """
    接口详细信息序列化
    """
    First = ApiInfoSerializer(many=True, read_only=True)

    class Meta:
        model = ApiGroupLevelFirst
        fields = ('id', 'name', 'First')


class ApiInfoListSerializer(serializers.ModelSerializer):
    """
    接口信息序列化
    """
    lastUpdateTime = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    userUpdate = serializers.CharField(source='userUpdate.first_name')

    class Meta:
        model = ApiInfo
        fields = ('id', 'name', 'requestType', 'apiAddress', 'mockStatus', 'lastUpdateTime', 'userUpdate')


class APIRequestHistorySerializer(serializers.ModelSerializer):
    """
    接口请求历史信息序列化
    """
    requestTime = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)

    class Meta:
        model = APIRequestHistory
        fields = ('id', 'requestTime', 'requestType', 'requestAddress', 'httpCode')


class APIRequestHistoryDeserializer(serializers.ModelSerializer):
    """
    接口请求历史信息反序列化
    """

    class Meta:
        model = APIRequestHistory
        fields = ('id', 'api_id', 'requestTime', 'requestType', 'requestAddress', 'httpCode')


class ApiOperationHistorySerializer(serializers.ModelSerializer):
    """
    接口操作历史信息序列化
    """
    time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    user = serializers.CharField(source='user.first_name')

    class Meta:
        model = ApiOperationHistory
        fields = ('id', 'user', 'time', 'description')


class ApiOperationHistoryDeserializer(serializers.ModelSerializer):
    """
    接口操作历史信息反序列化
    """

    class Meta:
        model = ApiOperationHistory
        fields = ('id', 'apiInfo', 'user', 'time', 'description')


class AutomationGroupLevelFirstSerializer(serializers.ModelSerializer):
    """
    自动化用例一级分组信息序列化
    """

    class Meta:
        model = AutomationGroupLevelFirst
        fields = ('id', 'project_id', 'name')


class AutomationTestCaseSerializer(serializers.ModelSerializer):
    """
    自动化用例信息序列化
    """
    updateTime = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    createUser = serializers.CharField(source='user.first_name')

    class Meta:
        model = AutomationTestCase
        fields = ('id', 'automationGroupLevelFirst', 'caseName', 'createUser',
                  'description', 'updateTime')


class AutomationTestCaseDeserializer(serializers.ModelSerializer):
    """
    自动化用例信息反序列化
    """

    class Meta:
        model = AutomationTestCase
        fields = ('id', 'project_id', 'automationGroupLevelFirst', 'caseName', 'user',
                  'description', 'updateTime')


class AutomationHeadSerializer(serializers.ModelSerializer):
    """
    自动化用例接口请求头信息序列化
    """

    class Meta:
        model = AutomationHead
        fields = ('id', 'automationCaseApi', 'name', 'value', 'interrelate')


class AutomationHeadDeserializer(serializers.ModelSerializer):
    """
    自动化用例接口请求头信息反序列化
    """

    class Meta:
        model = AutomationHead
        fields = ('id', 'automationCaseApi_id', 'name', 'value', 'interrelate')


class AutomationParameterSerializer(serializers.ModelSerializer):
    """
    自动化用例接口请求参数信息序列化
    """

    class Meta:
        model = AutomationParameter
        fields = ('id', 'automationCaseApi', 'name', 'value', 'interrelate')


class AutomationParameterDeserializer(serializers.ModelSerializer):
    """
    自动化用例接口请求参数信息反序列化
    """

    class Meta:
        model = AutomationParameter
        fields = ('id', 'automationCaseApi_id', 'name', 'value', 'interrelate')


class AutomationParameterRawSerializer(serializers.ModelSerializer):
    """
    接口请求参数源数据序列化
    """

    class Meta:
        model = AutomationParameterRaw
        fields = ('id', 'automationCaseApi', 'data')


class AutomationParameterRawDeserializer(serializers.ModelSerializer):
    """
    接口请求参数源数据反序列化
    """

    class Meta:
        model = AutomationParameterRaw
        fields = ('id', 'automationCaseApi_id', 'data')


class AutomationResponseJsonSerializer(serializers.ModelSerializer):
    """
    返回JSON参数序列化
    """

    class Meta:
        model = AutomationResponseJson
        fields = ('id', 'automationCaseApi', 'name', 'tier')


class AutomationResponseJsonDeserializer(serializers.ModelSerializer):
    """
    返回JSON参数反序列化
    """

    class Meta:
        model = AutomationResponseJson
        fields = ('id', 'automationCaseApi', 'name', 'tier')


class CorrelationDataSerializer(serializers.ModelSerializer):
    """
    关联数据序列化
    """
    response = AutomationResponseJsonSerializer(many=True, read_only=True)

    class Meta:
        model = AutomationCaseApi
        fields = ("id", "name", "response")


class AutomationCaseApiSerializer(serializers.ModelSerializer):
    """
    自动化用例接口详细信息序列化
    """
    header = AutomationHeadSerializer(many=True, read_only=True)
    parameterList = AutomationParameterSerializer(many=True, read_only=True)
    parameterRaw = AutomationParameterRawSerializer(many=False, read_only=True)

    class Meta:
        model = AutomationCaseApi
        fields = ('id', 'name', 'httpType', 'requestType', 'apiAddress', 'header', 'requestParameterType', 'formatRaw',
                  'parameterList', 'parameterRaw', 'examineType', 'httpCode', 'responseData')


class AutomationCaseDownloadSerializer(serializers.ModelSerializer):
    """
    下载用例读取数据序列
    """
    # api = AutomationCaseApiSerializer(many=True, read_only=True)
    updateTime = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    # automationGroupLevelFirst = serializers.CharField(source='automationGroupLevelFirst.name')
    user = serializers.CharField(source="user.first_name")
    api = serializers.SerializerMethodField()

    class Meta:
        model = AutomationTestCase
        fields = ('caseName', 'user', 'updateTime', 'api')

    def get_api(self, obj):
        return AutomationCaseApiSerializer(
            AutomationCaseApi.objects.filter(automationTestCase=obj).order_by("id"),
            many=True
        ).data


class AutomationCaseDownSerializer(serializers.ModelSerializer):
    """
    下载用例读取数据序列
    """
    automationGroup = AutomationCaseDownloadSerializer(many=True, read_only=True)

    class Meta:
        model = AutomationGroupLevelFirst
        fields = ("name", "automationGroup")


class AutomationCaseApiDeserializer(serializers.ModelSerializer):
    """
    自动化用例接口详细信息反序列化
    """

    class Meta:
        model = AutomationCaseApi
        fields = (
            'id', 'automationTestCase_id', 'name', 'httpType', 'requestType', 'apiAddress', 'requestParameterType',
            'formatRaw', 'examineType', 'httpCode', 'responseData')


class AutomationCaseApiListSerializer(serializers.ModelSerializer):
    """
    自动化用例接口列表信息序列化
    """

    class Meta:
        model = AutomationCaseApi
        fields = ('id', 'name', 'requestType', 'apiAddress')


class AutomationTestTaskSerializer(serializers.ModelSerializer):
    """
    定时任务信息序列化
    """
    startTime = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    endTime = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)

    class Meta:
        model = AutomationTestTask
        fields = ('id', 'project', 'Host', 'name', 'type', 'frequency', 'unit', 'startTime', 'endTime')


class AutomationTestTaskDeserializer(serializers.ModelSerializer):
    """
    定时任务信息反序列化
    """

    class Meta:
        model = AutomationTestTask
        fields = ('id', 'project_id', 'Host_id', 'name', 'type', 'frequency', 'unit', 'startTime', 'endTime')


class AutomationTestReportSerializer(serializers.ModelSerializer):
    """
    测试报告测试结果信息序列化
    """
    result = serializers.CharField(source='test_result.result')
    host = serializers.CharField(source='test_result.host')
    parameter = serializers.CharField(source='test_result.parameter')
    httpStatus = serializers.CharField(source='test_result.httpStatus')
    responseData = serializers.CharField(source='test_result.responseData')
    automationTestCase = serializers.CharField(source='automationTestCase.caseName')
    testTime = serializers.CharField(source='test_result.testTime')

    class Meta:
        model = AutomationCaseApi
        fields = ('id', 'automationTestCase', 'name', 'host', 'httpType', 'requestType', 'apiAddress', 'examineType',
                  'result', 'parameter', 'httpStatus', 'responseData', 'testTime')


class AutomationTaskRunTimeSerializer(serializers.ModelSerializer):
    """
    任务执行时间
    """
    startTime = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    project = serializers.CharField(source='project.name')

    class Meta:
        model = AutomationTaskRunTime
        fields = ('id', 'project', 'startTime', 'elapsedTime', 'host')


class AutomationTestResultSerializer(serializers.ModelSerializer):
    """
    手动测试结果详情序列化
    """
    testTime = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)

    class Meta:
        model = AutomationTestResult
        fields = ('id', 'url', 'requestType', 'header', 'parameter', 'statusCode', 'examineType', 'data',
                  'result', 'httpStatus', 'responseData', 'testTime')


class AutomationAutoTestResultSerializer(serializers.ModelSerializer):
    """
    自动测试结果详情序列化
    """

    name = serializers.CharField(source='automationCaseApi.name')
    httpType = serializers.CharField(source='automationCaseApi.httpType')
    requestType = serializers.CharField(source='automationCaseApi.requestType')
    apiAddress = serializers.CharField(source='automationCaseApi.apiAddress')
    examineType = serializers.CharField(source='automationCaseApi.examineType')
    automationTestCase = serializers.CharField(source='automationCaseApi.automationTestCase')

    class Meta:
        model = AutomationCaseTestResult
        fields = ('id', 'automationTestCase', 'name', 'httpType', 'header', 'requestType', 'apiAddress', 'examineType',
                  'result', 'parameter', 'httpStatus', 'responseHeader', 'responseData', 'testTime')


class AutomationTestLatelyTenTimeSerializer(serializers.ModelSerializer):
    """
    最近10次测试结果
    """

    class Meta:
        model = AutomationTaskRunTime
        fields = ("id", "startTime")


class AutomationReportSendConfigSerializer(serializers.ModelSerializer):
    """
    发送人配置序列
    """
    project = serializers.CharField(source='project.name')

    class Meta:
        model = AutomationReportSendConfig
        fields = ("id", "project", 'reportFrom', 'mailUser', 'mailPass', 'mailSmtp')


class AutomationReportSendConfigDeserializer(serializers.ModelSerializer):
    """
    发送人配置反序列
    """

    class Meta:
        model = AutomationReportSendConfig
        fields = ("id", "project_id", 'reportFrom', 'mailUser', 'mailPass', 'mailSmtp')


class test_report_Serializer(serializers.ModelSerializer):
    """
    郵件報告信息序列化
     """

    class Meta:
        model = test_report
        fields = (
            'report_id', 'test_version', 'cns_version', 'type', 'send_time', 'title', 'receiver', 'email_cc',
            'content_id',
            'update_time', 'create_time')
        read_only_fields = ('report_id',)  # 指定只读的 field

    def get_apiCount(self, obj):
        return obj.api_project.all().count()

    def get_dynamicCount(self, obj):
        return obj.dynamic_project.all().count()

    def get_memberCount(self, obj):
        return obj.member_project.all().count()


class test_report_Deserializer(serializers.ModelSerializer):
    """
    郵件報告信息反序列化
    """

    class Meta:
        model = test_report
        fields = ('test_version', 'cns_version', 'type', 'send_time', 'title', 'receiver', 'email_cc', 'content_id')


class test_risk_Serializer(serializers.ModelSerializer):
    """
    测试风险序列化
     """

    class Meta:
        model = test_risk
        fields = ('risk_id', 'project_id', 'risk', 'development', 'delay', 'solution_status', 'status',
                  'update_time', 'create_time')
        read_only_fields = ('owner',)  # 指定只读的 field

    def get_apiCount(self, obj):
        return obj.api_project.all().count()

    def get_dynamicCount(self, obj):
        return obj.dynamic_project.all().count()

    def get_memberCount(self, obj):
        return obj.member_project.all().count()


class test_risk_Deserializer(serializers.ModelSerializer):
    """
    测试风险反序列化
    """

    class Meta:
        model = test_risk
        fields = ('risk_id', 'project_id', 'risk', 'development', 'delay', 'solution_status', 'status')


class base_data_Serializer(serializers.ModelSerializer):
    """
    基础信息序列化
     """

    class Meta:
        model = base_data
        fields = (
        'id', 'content', 'type', 'select_type', 'status', 'predictor', 'remarks', 'other', 'update_time', 'create_time')
        read_only_fields = ('id',)  # 指定只读的 field

    def get_apiCount(self, obj):
        return obj.api_project.all().count()

    def get_dynamicCount(self, obj):
        return obj.dynamic_project.all().count()

    def get_memberCount(self, obj):
        return obj.member_project.all().count()


class base_data_Deserializer(serializers.ModelSerializer):
    """
    基础信息反序列化
    """

    class Meta:
        model = base_data
        fields = ('content', 'type', 'select_type', 'status', 'remarks', 'other')


class stress_Serializer(serializers.ModelSerializer):
    """
    性能测试记录表序列化
     """

    class Meta:
        model = stress
        fields = (
        'id', 'projectname', 'version', 'thread', 'synchroniz', 'ramp', 'loop_count', 'duration', 'start_delay',
        'dicom_send',
        'loadserver', 'testdata', 'loop_time', 'start_date', 'end_date','jmeterstatus', 'status', 'update_time', 'create_time')
        read_only_fields = ('id',)  # 指定只读的 field

    def get_apiCount(self, obj):
        return obj.api_project.all().count()

    def get_dynamicCount(self, obj):
        return obj.dynamic_project.all().count()

    def get_memberCount(self, obj):
        return obj.member_project.all().count()


class stress_Deserializer(serializers.ModelSerializer):
    """
    性能测试记录表反序列化
    """

    class Meta:
        model = stress
        fields = (
        'id', 'projectname', 'version', 'loadserver', 'testdata', 'thread', 'synchroniz', 'ramp', 'loop_count',
        'duration', 'start_delay', 'dicom_send',
        'loop_time', 'start_date', 'end_date','jmeterstatus', 'status')


class dicomrecord_Serializer(serializers.ModelSerializer):
    """
    测试数据记录表序列化

     """

    class Meta:
        model = dicom_record
        fields = ('id', 'version','server', 'patientid', 'studyinstanceuid', 'slicenumber',
                  'diseases', 'aidiagnosis', 'aistatus', 'diagnosis', 'starttime', 'completiontime', 'type',
                  'report', 'status', 'update_time', 'create_time')
        read_only_fields = ('id',)  # 指定只读的 field

    def get_apiCount(self, obj):
        return obj.api_project.all().count()

    def get_dynamicCount(self, obj):
        return obj.dynamic_project.all().count()

    def get_memberCount(self, obj):
        return obj.member_project.all().count()


class dicomrecord_Deserializer(serializers.ModelSerializer):
    """
    测试数据记录表反序列化
    """

    class Meta:
        model = dicom_record
        fields = ('version','server', 'patientid', 'studyinstanceuid', 'slicenumber',
                  'diseases', 'aidiagnosis', 'aistatus', 'diagnosis', 'starttime', 'completiontime', 'type',
                  'report', 'status')


class stress_result_Serializer(serializers.ModelSerializer):
    """
    性能测试数据记录表序列化
     """

    class Meta:
        model = stress_result
        fields = ('id', 'version', 'modelname', 'type', 'slicenumber', 'count', 'avg',
                  'single', 'median', 'min', 'max', 'coef', 'rate', 'minimages', 'maximages', 'avgimages',
                  'update_time', 'create_time')
        read_only_fields = ('id',)  # 指定只读的 field

    def get_apiCount(self, obj):
        return obj.api_project.all().count()

    def get_dynamicCount(self, obj):
        return obj.dynamic_project.all().count()

    def get_memberCount(self, obj):
        return obj.member_project.all().count()


class stress_result_Deserializer(serializers.ModelSerializer):
    """
    性能测试数据记录表反序列化
    """

    class Meta:
        model = stress_result
        fields = ('version', 'modelname', 'type', 'slicenumber', 'count', 'avg',
                  'single', 'median', 'min', 'max', 'coef', 'rate', 'minimages', 'maximages', 'avgimages')


class duration_record_Serializer(serializers.ModelSerializer):
    """
    持续化测试记录表序列化
     """

    class Meta:
        model = duration_record
        fields = (
            'id', 'patientid', 'accessionnumber', 'studyinstanceuid', 'studyolduid', 'imagecount', 'imagecount_server',
            'aistatus',
            'diagnosis', 'sendserver', 'duration_id', 'sendtime','time','endtime', 'update_time', 'create_time')
        read_only_fields = ('id',)  # 指定只读的 field

    def get_apiCount(self, obj):
        return obj.api_project.all().count()

    def get_dynamicCount(self, obj):
        return obj.dynamic_project.all().count()

    def get_memberCount(self, obj):
        return obj.member_project.all().count()


class duration_record_Deserializer(serializers.ModelSerializer):
    """
    持续化反序列化
    """

    class Meta:
        model = duration_record
        fields = (
        'id', 'patientid', 'accessionnumber', 'studyinstanceuid', 'studyolduid', 'imagecount', 'imagecount_server',
        'aistatus',
        'diagnosis', 'sendserver', 'duration_id', 'sendtime','time','endtime','create_time')


class duration_Serializer(serializers.ModelSerializer):
    """
    持续化测试记录表序列化
     """

    class Meta:
        model = duration
        fields = (
            'id', 'server', 'port', 'aet', 'keyword', 'dicom', 'end_time', 'sleepcount', 'sleeptime', 'series',
            'sendstatus', 'status', 'sendcount', 'dds', 'update_time', 'create_time')
        read_only_fields = ('id',)  # 指定只读的 field

    def get_apiCount(self, obj):
        return obj.api_duration.all().count()

    def get_dynamicCount(self, obj):
        return obj.dynamic_duration.all().count()

    def get_memberCount(self, obj):
        return obj.member_duration.all().count()


class duration_Deserializer(serializers.ModelSerializer):
    """
    持续化反序列化
    """

    class Meta:
        model = duration
        fields = (
        'server', 'port', 'aet', 'keyword', 'dicom', 'end_time', 'sleepcount', 'sleeptime', 'series', 'sendstatus',
        'status', 'sendcount', 'dds')


class dicomdata_Deserializer(serializers.ModelSerializer):
    """
    持续化记录表反序列化
    """

    class Meta:
        model = dicom
        fields = (
        'id', 'patientid', 'studyinstanceuid', 'diseases', 'slicenumber', 'vote', 'server', 'imagecount', 'fileid',
        'diagnosis', 'type', 'route')


class dictionary_Serializer(serializers.ModelSerializer):
    """
    字典序列化
     """
    class Meta:
        model = dictionary
        fields = ('id', 'key', 'value', 'remarks', 'type', 'status')
        read_only_fields = ('id',)  # 指定只读的 field

    def get_apiCount(self, obj):
        return obj.api_project.all().count()


    def get_dynamicCount(self, obj):
        return obj.dynamic_project.all().count()


    def get_memberCount(self, obj):
        return obj.member_project.all().count()


class dictionary_Deserializer(serializers.ModelSerializer):
    """
    字典反序列化
    """

    class Meta:
        model = dictionary
        fields = ('id', 'key', 'value', 'remarks', 'type', 'status')


class uploadfile_Deserializer(serializers.ModelSerializer):
    """
    字典反序列化
    """

    class Meta:
        model = uploadfile
        fields = ('id', 'filename', 'fileurl', 'fileid', 'type', 'status', 'update_time', 'create_time')
