#! /usr/bin/env python
# -*- coding: utf-8
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.authtoken.models import Token

from .models import *


class autoui_Serializer(serializers.ModelSerializer):
    """
    自动化测试列表列化
     """
    class Meta:
        model = autoui
        fields = ('autoid', 'version', 'setup','cases','tearDown','progress', 'thread', 'starttime', 'completiontime', 'total', 'Host', 'report', 'type', 'status')
        read_only_fields = ('autoid',)  # 指定只读的 field


class autoui_Deserializer(serializers.ModelSerializer):
    """
    自动化测试列表反序列化
    """

    class Meta:
        model = autoui
        fields = ('version', 'setup', 'cases', 'tearDown', 'progress', 'thread', 'starttime', 'completiontime', 'total', 'status', 'Host', 'report', 'type')


class autorecord_Serializer(serializers.ModelSerializer):
    """
    AutoTest测试数据记录表序列化

     """

    class Meta:
        model = auto_uirecord
        fields = ('id', 'studyuid',  'vote', 'expect','actual', 'aistatus',  'starttime', 'completiontime', 'type',
                  'result', 'status', 'case', 'server', 'dicomid', 'auto', 'update_time', 'create_time')
        read_only_fields = ('id',)  # 指定只读的 field



class autorecord_Deserializer(serializers.ModelSerializer):
    """
    AutoTest测试数据记录表反序列化
    """
    class Meta:
        model = auto_uirecord
        fields = ('studyuid',  'vote', 'expect','actual', 'aistatus',  'starttime', 'completiontime', 'type',
                  'result', 'status','case', 'server', 'auto', 'dicomid')

class autocase_Serializer(serializers.ModelSerializer):
    """
    auto_case表序列化

     """

    class Meta:
        model = auto_uicase
        fields = ('id', 'name',  'testdata', 'type', 'status','update_time', 'create_time')
        read_only_fields = ('id',)  # 指定只读的 field



class autocase_Deserializer(serializers.ModelSerializer):
    """
    auto_case表反序列化
    """
    class Meta:
        model = auto_uicase
        fields = ('name',  'testdata', 'type','status')

