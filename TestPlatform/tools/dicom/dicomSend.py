# coding=utf-8
'''
作用：
把文件夹中的所有study，匿名成不同的uid，持续发到storescp中。
参数说明：
1，CONFIG.local：本storescu的信息，包括ae title
2，CONFIG.server：storescp的信息，包括ae title、ip、port
3，CONFIG.keyword：发送文件匿名tags（patientID, patientName）的前缀关键词
4，CONFIG.dicomfolder：需要发送dicom文件的所在目录
'''

import os
import pydicom
from tqdm import tqdm
import shutil
import subprocess as sp
import time,datetime
import random
import math
import pymysql
import logging
from django.db import transaction
from django.conf import settings

from TestPlatform.serializers import duration_record_Deserializer, duration_record_Serializer
logger = logging.getLogger(__name__)  # 这里使用 __name__ 动态搜索定义的 logger 配置。

# 下面只是个数据结构示例，具体的值会采用命令行传进来的
CONFIG = {
    'local': {
        'aet': 'QA38'
    },
    'server': {
        'aet': 'ORTHANC',
        'ip': '192.168.1.208',
        'port': '4242'
    },
    'keyword': 'duration',
    'dicomfolder': '/home/biomind/testDatas'
}



def sync_send(folder,server_ip,server_aet):
    if not folder or not os.path.exists(folder):
        logger.info('send: path is not exist [{0}]'.format(folder))
        return

    file_names = os.listdir(folder)
    file_names.sort()

    logger.info(' sending: {0}'.format(folder))
    for fn in tqdm(file_names):
        full_fn = os.path.join(folder, fn)

        if (fn == '.DS_Store'):
            continue
        elif (os.path.isdir(full_fn)):
            sync_send(full_fn)
            continue
        try:
            commands = [
                "storescu",
                server_ip,
                '4242',
                "-aec", server_aet,
                "-aet", 'QA38',
                full_fn
            ]

            try:
                popen = sp.Popen(commands, stderr=sp.PIPE, stdout=sp.PIPE, shell=False)
                popen.communicate()
            except Exception as e:
                logger.error('send_file error: {0}'.format(e))
        except Exception as e:
            logger.error(
                'failed to send file: file[{0}], error[{1}]'.format(full_fn, e))
            continue


def fake_folder(folder):
    file_names = os.listdir(folder)
    file_names.sort()

    for fn in tqdm(file_names):
        full_fn = os.path.join(folder, fn)
        if (fn == '.DS_Store'):
            continue
        elif (os.path.isdir(full_fn)):
            fake_folder(full_fn)
            continue
        try:
            ds = pydicom.dcmread(full_fn, force=True)
        except Exception as e:
            logger.error('errormsg: failed to read file [{0}]'.format(full_fn))
            continue
        try:
            study_uid = ds.StudyInstanceUID
            stressserializer = duration_record_Serializer(data=study_uid)
            with transaction.atomic():
                stressserializer.is_valid()
                stressserializer.save()
        except Exception as e:
            logger.info(
                'failed to fake studyinstanceuid: file[{0}], error[{1}]'.format(full_fn, e))
            continue





def sendDicom(server_ip,dicomfolder):

    logger.info('start to send: path[{0}]'.format(dicomfolder))

    src_folder = dicomfolder
    while src_folder[-1] == '/':
        src_folder = src_folder[0:-1]

    sync_send(src_folder)
    shutil.rmtree(src_folder)

