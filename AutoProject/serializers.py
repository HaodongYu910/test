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
    userID = serializers.CharField(source="user.id")
    username = serializers.CharField(source="user.username")
    first_name = serializers.CharField(source="user.first_name")
    last_name = serializers.CharField(source="user.last_name")
    phone = serializers.CharField(source="user.user.phone")
    email = serializers.CharField(source="user.email")
    roles = serializers.CharField(source="user.user.roles")
    userphoto = serializers.CharField(source="user.user.userphoto")
    date_joined = serializers.CharField(source="user.date_joined")

    class Meta:
        model = Token
        fields = (
        'userID', 'username', 'first_name', 'last_name', 'phone', 'email', 'key', 'roles', 'userphoto', 'date_joined')


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
            'id', 'name', 'type', 'status', 'start_date',
            'end_date', 'client', 'description', 'LastUpdateTime', 'createTime', 'user')


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
            'id', 'name', 'type', 'status', 'start_date',
            'end_date',
            'client', 'LastUpdateTime', 'createTime', 'apiCount',
            'dynamicCount', 'memberCount', 'description', 'user')

    def get_apiCount(self, obj):
        return obj.api_project.all().count()

    def get_dynamicCount(self, obj):
        return obj.dynamic_project.all().count()

    def get_memberCount(self, obj):
        return obj.member_project.all().count()


class ProjectVersionDeserializer(serializers.ModelSerializer):
    """
    项目版本信息反序列化
    """

    class Meta:
        model = project_version
        fields = (
            'id', 'version', 'branch', 'package_name', 'path', 'type', 'project', 'status', 'update_time',
            'create_time')


class ProjectVersionSerializer(serializers.ModelSerializer):
    """
    项目版本版本信息序列化
    """
    # project = serializers.CharField(source='Project.name')
    update_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    create_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)

    class Meta:
        model = project_version
        fields = (
            'id', 'version', 'branch', 'package_name', 'path', 'type', 'project', 'status', 'update_time',
            'create_time')


class ProjectDynamicDeserializer(serializers.ModelSerializer):
    """
    项目动态信息反序列化
    """

    class Meta:
        model = ProjectDynamic
        fields = ('id', 'project', 'module', 'time', 'type', 'operationObject', 'user', 'description')


class ProjectDynamicSerializer(serializers.ModelSerializer):
    """
    项目动态信息序列化
    """
    operationUser = serializers.CharField(source='user.first_name')
    time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)

    class Meta:
        model = ProjectDynamic
        fields = ('id', 'time', 'type', 'module', 'operationObject', 'operationUser', 'description')


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


class ServerSerializer(serializers.ModelSerializer):
    """
    host信息序列化
    """

    class Meta:
        model = Server
        fields = (
            'id', 'project_id', 'name', 'host', 'port', 'user', 'pwd', 'remarks', 'description', 'protocol', 'status')


class dictionary_Serializer(serializers.ModelSerializer):
    """
    字典序列化
     """

    class Meta:
        model = dictionary
        fields = ('id', 'key', 'value', 'remarks', 'type', 'status')
        read_only_fields = ('id',)  # 指定只读的 field


class dictionary_Deserializer(serializers.ModelSerializer):
    """
    字典反序列化
    """

    class Meta:
        model = dictionary
        fields = ('id', 'key', 'value', 'remarks', 'type', 'status')


class uploadfile_Deserializer(serializers.ModelSerializer):
    """
    上传文件反序列化
    """

    class Meta:
        model = uploadfile
        fields = ('id', 'filename', 'fileurl', 'fileid', 'type', 'status', 'remark', 'update_time', 'create_time')


class install_Deserializer(serializers.ModelSerializer):
    """
    安装反序列化
    """

    class Meta:
        model = install
        fields = (
            'id', 'server', 'testcase', 'version', 'starttime', 'Host', 'smokeid', 'uid', 'type', 'status',
            'installstatus',
            'crontab')


class build_packageDeserializer(serializers.ModelSerializer):
    """
    打包部署信息反序列化
    """

    class Meta:
        model = build_package
        fields = (
            'id', 'name',  'type', 'code', 'branch', 'status', 'crontab', 'git',
            'packStatus', 'rely', 'Host', 'create_time', 'update_time', 'user', 'build_status')


class build_packageSerializer(serializers.ModelSerializer):
    """
    打包部署 信息序列化
    """
    update_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    create_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    service = serializers.CharField(source='git.name')
    user = serializers.CharField(source='user.first_name')
    jenkins_job = serializers.CharField(source='git.jenkins_job')
    jenkins_view = serializers.CharField(source='git.jenkins_view')

    class Meta:
        model = build_package
        fields = (
            'id', 'name', 'service', 'type', 'code', 'branch', 'status', 'crontab', 'git', 'jenkins_job',
            'packStatus', 'rely', 'Host', 'create_time', 'update_time', 'user', 'jenkins_view', 'build_status'
        )


class build_package_detailDeserializer(serializers.ModelSerializer):
    """
    打包部署详情信息反序列化
    """

    class Meta:
        model = build_package_detail
        fields = (
            'id', 'name', 'type', 'code', 'branch', 'status', 'crontab',
            'packStatus', 'rely', 'Host', 'job', 'build', 'create_time', 'update_time', 'user')

class build_package_detailSerializer(serializers.ModelSerializer):
    """
    打包部署详情 信息序列化
    """
    update_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    create_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    # Host = serializers.CharField(source='Host.host')
    user = serializers.CharField(source='user.username')

    class Meta:
        model = build_package_detail
        fields = (
            'id', 'name', 'type', 'code', 'branch', 'status', 'crontab',
            'packStatus', 'rely', 'Host', 'create_time', 'update_time', 'user', 'job', 'build',
        )


class project_git_Deserializer(serializers.ModelSerializer):
    """
    项目仓库信息反序列化
    """

    class Meta:
        model = project_git
        fields = (
            'id', 'name', 'gitname', 'jenkin_view', 'jenkins_job', 'code', 'Project', 'status', 'create_time', 'update_time', 'user')


class project_git_Serializer(serializers.ModelSerializer):
    """
    项目仓库信息 信息序列化
    """
    update_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    create_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    Project = serializers.CharField(source='Project.name')
    user = serializers.CharField(source='user.username')

    class Meta:
        model = project_git
        fields = (
            'id', 'name', 'gitname', 'jenkins_view', 'jenkins_job', 'code', 'Project', 'status', 'create_time', 'update_time', 'user'
        )
