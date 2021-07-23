#! /usr/bin/env python
# -*- coding: utf-8
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.authtoken.models import Token

from .models import *


class dicom_detail_Serializer(serializers.ModelSerializer):
    """
    基础信息序列化
     """

    class Meta:
        model = dicom_detail
        fields = (
            'id', 'content', 'type', 'select_type', 'status', 'predictor', 'remarks', 'other', 'update_time',
            'create_time')
        read_only_fields = ('id',)  # 指定只读的 field


class dicom_detail_Deserializer(serializers.ModelSerializer):
    """
    基础信息反序列化
    """

    class Meta:
        model = dicom_detail
        fields = ('content', 'type', 'select_type', 'status', 'remarks', 'other')


class dicomdata_Deserializer(serializers.ModelSerializer):
    """
    dicom数据表反序列化
    """

    class Meta:
        model = dicom
        fields = (
            'id', 'patientid', 'patientname', 'studyinstanceuid', 'diseases', 'slicenumber', 'vote', 'graphql',
            'predictor', 'imagecount', 'fileid',
            'diagnosis', 'remark', 'type', 'route', 'status', 'stressstatus')


class duration_record_Serializer(serializers.ModelSerializer):
    """
    持续化测试记录表序列化
     """

    class Meta:
        model = duration_record
        fields = (
            'id', 'patientid', 'patientname', 'studyinstanceuid', 'studyolduid', 'image',
            'image_receive', 'sec', 'start', 'end', 'job_sec', 'job_start', 'job_end',
            'aistatus', 'diagnosis', 'slicenumber', 'relation_id', 'type', 'status'
            'diseases', 'Host', 'error', 'model', 'update_time', 'create_time')
        read_only_fields = ('id',)  # 指定只读的 field

class duration_record_Deserializer(serializers.ModelSerializer):

    """
    持续化反序列化
    """

    class Meta:
        model = duration_record
        fields = (
            'id', 'patientid', 'patientname', 'studyinstanceuid', 'studyolduid', 'image',
            'image_receive', 'sec', 'start', 'end', 'job_sec', 'job_start', 'job_end',
            'aistatus', 'diagnosis', 'slicenumber', 'relation_id', 'type', 'status',
            'diseases', 'Host', 'error', 'model')

class duration_Serializer(serializers.ModelSerializer):
    """
    持续化测试记录表序列化
     """

    class Meta:
        model = duration
        fields = (
            'id', 'version', 'server', 'port', 'aet', 'patientname', 'patientid', 'dicom', 'end_time', 'sleepcount',
            'sleeptime', 'series', 'project', 'sendstatus', 'status', 'sendcount', 'group', 'dds', 'type', 'Host',
            'update_time', 'create_time')
        read_only_fields = ('id',)  # 指定只读的 field


class duration_Deserializer(serializers.ModelSerializer):
    """
    持续化反序列化
    """

    class Meta:
        model = duration
        fields = [
            'id', 'version', 'server', 'port', 'aet', 'patientname', 'patientid', 'dicom', 'end_time', 'sleepcount',
            'sleeptime', 'series',
            'sendstatus', 'status', 'sendcount', 'group', 'dds', 'type', 'Host', 'project']


class dicomGroup_Serializer(serializers.ModelSerializer):
    """
    组基础信息序列化
     """

    class Meta:
        model = dicom_group
        fields = (
            'id', 'name', 'group', 'amount', 'route', 'predictor', 'type', 'remark', 'status', 'update_time',
            'create_time', 'project')
        read_only_fields = ('id',)  # 指定只读的 field


class dicomGroup_detail_Deserializer(serializers.ModelSerializer):
    """
    组详细信息反序列化
    """

    class Meta:
        model = dicom_group_detail
        fields = ('id', 'dicom', 'group')
