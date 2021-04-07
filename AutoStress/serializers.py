#! /usr/bin/env python
# -*- coding: utf-8
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.authtoken.models import Token

from .models import *


class stress_Serializer(serializers.ModelSerializer):
    """
    性能测试记录表序列化
     """

    class Meta:
        model = stress
        fields = (
        'stressid', 'projectname', 'version', 'thread', 'synchroniz', 'ramp', 'loop_count', 'duration', 'start_delay',
        'dicom_send',
        'loadserver', 'testdata', 'loop_time', 'start_date', 'end_date','jmeterstatus', 'status','Host', 'update_time', 'create_time')
        read_only_fields = ('stressid',)  # 指定只读的 field

class stress_Deserializer(serializers.ModelSerializer):
    """
    性能测试记录表反序列化
    """

    class Meta:
        model = stress
        fields = (
        'stressid', 'projectname', 'version', 'loadserver', 'testdata', 'thread', 'synchroniz', 'ramp', 'loop_count',
        'duration', 'start_delay', 'dicom_send',
        'loop_time', 'start_date', 'end_date','jmeterstatus', 'status','Host')


class stress_result_Serializer(serializers.ModelSerializer):
    """
    性能测试数据记录表序列化
     """

    class Meta:
        model = stress_result
        fields = ('id', 'version', 'modelname', 'type', 'slicenumber', 'count', 'avg',
                  'single', 'median', 'min', 'max', 'coef', 'rate', 'minimages', 'maximages', 'avgimages','Stress',
                  'update_time', 'create_time')
        read_only_fields = ('id',)  # 指定只读的 field


class stress_result_Deserializer(serializers.ModelSerializer):
    """
    性能测试数据记录表反序列化
    """

    class Meta:
        model = stress_result
        fields = ('version', 'modelname', 'type', 'slicenumber', 'count', 'avg',
                  'single', 'median', 'min', 'max', 'coef', 'rate', 'minimages', 'maximages', 'avgimages', 'Stress')



class stress_record_Deserializer(serializers.ModelSerializer):
    """
    性能测试记录反序列化
    """
    class Meta:
        model = stress_record
        fields = ('id', 'Stress', 'studyuid', 'slicenumber', 'image', 'version',
                  'type', 'job_id', 'sec','start', 'end', 'modelname','aistatus')

class stress_record_Serializer(serializers.ModelSerializer):
    """
    性能测试记录序列化
     """

    class Meta:
        model = stress_record
        fields = ('id', 'Stress', 'studyuid', 'slicenumber', 'image', 'version',
                  'type', 'job_id', 'sec','start', 'end', 'modelname','aistatus')
        read_only_fields = ('id',)  # 指定只读的 field

class errorlog_Serializer(serializers.ModelSerializer):
    """
    性能测试错误日志记录序列化
     """

    class Meta:
        model = stress_record
        fields = ('id', 'Stress', 'content', 'route', 'version')
        read_only_fields = ('id',)  # 指定只读的 field
