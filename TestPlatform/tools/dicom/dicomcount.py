# coding=utf-8

import os
import pydicom
from tqdm import tqdm
import time,datetime
import random
import math
import logging
from TestPlatform.models import base_data

logger = logging.getLogger(__name__)  # 这里使用 __name__ 动态搜索定义的 logger 配置。

# 下面只是个数据结构示例，具体的值会采用命令行传进来的

def get_date():
    localtime = time.localtime(time.time())
    return (time.strftime("%Y-%m-%d", localtime))


def get_time():
    localtime = time.localtime(time.time())
    return (time.strftime("%H:%M:%S", localtime))


def get_rand_uid():
    rand_val = random.randint(1, math.pow(10, 8) - 1)
    return "%08d" % rand_val


def fake_folder(src_folder,study_infos):

    file_names = os.listdir(src_folder)
    file_names.sort()

    for fn in tqdm(file_names):
        full_fn = os.path.join(src_folder, fn)
        if (fn == '.DS_Store'):
            continue
        elif (os.path.isdir(full_fn)):
            fake_folder(full_fn,study_infos)
            continue
        try:
            ds = pydicom.dcmread(full_fn, force=True)
            StudyInstanceUID = ds.StudyInstanceUID
            study_infos.append(StudyInstanceUID)

        except Exception as e:
            logger.error('errormsg: failed to read file [{0}]'.format(full_fn))
            continue

    return list(set(study_infos))

def filecount(id):
    obj= base_data.objects.filter(id=id)

    for i in obj:
        folder=i.content
        study_infos = []
        src_folder = folder
        while src_folder[-1] == '/':
            src_folder = src_folder[0:-1]
        list=fake_folder(src_folder=src_folder,study_infos=study_infos)
        i.other =len(list)
        i.save()


def file_count(folder):
    study_infos = []
    src_folder = folder
    while src_folder[-1] == '/':
        src_folder = src_folder[0:-1]
    list=fake_folder(src_folder=src_folder,study_infos=study_infos)
    count =len(list)
    return count





