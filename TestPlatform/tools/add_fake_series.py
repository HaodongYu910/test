# coding=utf-8
'''
作用：
把文件夹中的所有study，匿名成不同的uid。
参数说明：
1，CONFIG.keyword：发送文件匿名tags（patientID, patientName）的前缀关键词
2，CONFIG.dicomfolder：dicom文件的所在目录
'''

import os
import sys, getopt
import pydicom
import logging
from tqdm import tqdm
import shutil
import subprocess as sp
from .stopwatch import stopwatch
import time
import random
import math
import csv
import codecs


log_path = './logs'
if not os.path.exists(log_path):
    os.makedirs(log_path)

# 下面只是个数据结构示例，具体的值会采用命令行传进来的
CONFIG = {
    'keyword': 'ctactp_',
    'sourcefolder': '/Users/chenjiwen/temp/cta_ctp_anony/cta_ctp_40000/CT iDose 3-2'
}


def get_date():
    localtime = time.localtime(time.time())
    return (time.strftime("%Y%m%d", localtime) )

def get_time():
    localtime = time.localtime(time.time())
    return (time.strftime("%H%M%S", localtime) )

def get_rand_uid():
    rand_val = random.randint(1, math.pow(10, 8)-1)
    return "%08d"%rand_val

def get_fake_name(rand_uid):
    fake_prefix = CONFIG["keyword"]
    return "{0}{1}".format(fake_prefix, rand_uid)


def norm_string(str, len_norm):
    str_dest = str
    while len(str_dest) > len_norm or str_dest[0] == '.':
        str_dest = str_dest[1:]
    return str_dest


def fake_series(folder, folder_fake, loop_times):
    if not os.path.exists(folder_fake):
        os.makedirs(folder_fake)

    file_names = os.listdir(folder)
    file_names.sort()

    rand_uid = get_rand_uid()

    for fn in tqdm(file_names):
        full_fn = os.path.join(folder, fn)
        full_fn_fake = os.path.join(folder_fake, fn)

        if (fn == '.DS_Store'):
            continue
        elif (os.path.isdir(full_fn)):
            fake_folder(full_fn, full_fn_fake, loop_times)
            continue
        try:
            ds = pydicom.dcmread(full_fn, force=True)
        except Exception as e:
            print('errormsg: failed to read file [{0}]'.format(full_fn))
            continue

        try:
            series_num = int(ds.SeriesNumber) + loop_times
        except Exception as e:
            logging.info(
                'failed to fake studyinstanceuid: file[{0}], error[{1}]'.format(full_fn, e))

        series_uid = ''
        try:
            series_uid = ds.SeriesInstanceUID
        except Exception as e:
            logging.info(
                'failed to fake seriesinstanceuid: file[{0}], error[{1}]'.format(full_fn, e))
        ds.SeriesInstanceUID = norm_string(
            '{0}.{1}'.format(series_uid, rand_uid), 64)

        instance_uid = ''
        try:
            instance_uid = ds.SOPInstanceUID
        except Exception as e:
            logging.info(
                'failed to fake sopinstanceuid: file[{0}], error[{1}]'.format(full_fn, e))
        ds.SOPInstanceUID = norm_string(
            '{0}.{1}'.format(instance_uid, rand_uid), 64)

        ds.SeriesNumber = '{0}'.format(series_num)
        ds.SeriesDescription = ''

        try:
            ds.save_as(full_fn_fake)

        except Exception as e:
            print('errormsg: failed to save file [{0}]'.format(full_fn_fake))
            continue


if __name__ == '__main__':

    folder = CONFIG.get('sourcefolder', '')
    logging.info('send: path[{0}]'.format(folder))

    src_folder = folder
    while src_folder[-1] == '/':
        src_folder = src_folder[0:-1]

    dest_folder = src_folder

    loop_times = 0

    while loop_times < 9:
        
        loop_times = loop_times + 1

        folder_fake = "{0}_{1}".format(dest_folder, loop_times)

        sw = stopwatch('faking: path[{0}]'.format(folder_fake), logging)

        fake_series(
            folder=src_folder, 
            folder_fake=folder_fake,
            loop_times=loop_times
        )
        sw.del_msg()

