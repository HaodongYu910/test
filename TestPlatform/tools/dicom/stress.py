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

import os,gc
import sys, getopt
import pydicom
import logging
from tqdm import tqdm
import subprocess as sp
import time, datetime
import random
import math


log_path = '/files/logs'
if not os.path.exists(log_path):
    os.makedirs(log_path)

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
    'dicomfolder': '/files/TestData/all/',
    'diseases': 'all',
    'end': ''
}


def get_date():
    localtime = time.localtime(time.time())
    return (time.strftime("%Y%m%d", localtime))


def get_time():
    localtime = time.localtime(time.time())
    return (time.strftime("%H%M%S", localtime))


def get_rand_uid():
    rand_val = random.randint(1, math.pow(10, 8) - 1)
    return "%08d" % rand_val


def get_fake_name(rand_uid):
    fake_prefix = CONFIG["keyword"]
    ts = time.localtime(time.time())
    return "{0}{1}{2}".format(fake_prefix, time.strftime("%m%d", ts), norm_string(rand_uid, 6))


def sync_send_file(file_name):
    # logging.info('send file: [{0}]'.format(file_name))
    commands = [
        "storescu",
        CONFIG.get('server', {}).get('ip'),
        CONFIG.get('server', {}).get('port'),
        "-aec", CONFIG.get('server', {}).get('aet'),
        "-aet", CONFIG.get('local', {}).get('aet'),
        file_name
    ]

    try:
        popen = sp.Popen(commands, stderr=sp.PIPE, stdout=sp.PIPE, shell=False)
        popen.communicate()
    except Exception as e:
        logging.error('send_file error: {0}'.format(e))


def norm_string(str, len_norm):
    str_dest = str
    while len(str_dest) > len_norm or str_dest[0] == '.':
        str_dest = str_dest[1:]
    return str_dest


def get_fake_accession_number(acc_number, rand_uid):
    str = "{0}_{1}".format(acc_number, rand_uid)
    return norm_string(str, 16)


def get_study_fakeinfo(studyuid, acc_number, studyuid_fakeinfo):
    if not studyuid_fakeinfo.get(studyuid):
        rand_uid = get_rand_uid()
        info = {
            "rand_uid": rand_uid,
            "fake_name": get_fake_name(rand_uid),
            "fake_acc_num": get_fake_accession_number(acc_number, rand_uid),
            "cur_date": get_date(),
            "cur_time": get_time()
        }
        studyuid_fakeinfo[studyuid] = info

    fake_info = studyuid_fakeinfo[studyuid]
    return fake_info



def fake_folder(folder, folder_fake):
    if not os.path.exists(folder_fake):
        os.makedirs(folder_fake)
    file_names = os.listdir(folder)
    file_names.sort()

    for fn in file_names:
        full_fn = os.path.join(folder, fn)
        full_fn_fake = os.path.join(folder_fake, fn)

        if (os.path.splitext(fn)[1] in  ['.dcm'] == False):
            continue
        elif (os.path.isdir(full_fn)):
            fake_folder(full_fn, full_fn_fake)
            continue
        try:
            ds = pydicom.dcmread(full_fn, force=True)
        except Exception as e:
            logging.error('errormsg: failed to read file [{0}]'.format(full_fn))
            continue

        study_uid = ''
        try:
            study_fakeinfos = {}
            study_uid = ds.StudyInstanceUID
            study_old_uid = ds.StudyInstanceUID
            Seriesinstanceuid=ds.SeriesInstanceUID
            acc_number = ds.AccessionNumber
            study_fakeinfo = get_study_fakeinfo(study_uid, acc_number, study_fakeinfos)
            rand_uid = study_fakeinfo.get("rand_uid")
            fake_name = study_fakeinfo.get("fake_name")
            fake_acc_number = study_fakeinfo.get("fake_acc_num")
            cur_date = study_fakeinfo.get("cur_date")
            cur_time = study_fakeinfo.get("cur_time")
        except Exception as e:
            logging.error(
                'failed to fake studyinstanceuid: file[{0}], error[{1}]'.format(full_fn, e))
            continue
        ds.StudyInstanceUID = norm_string(
            '{0}.{1}'.format(study_uid, rand_uid), 64)

        series_uid = ''
        try:
            series_uid = ds.SeriesInstanceUID
        except Exception as e:
            logging.error(
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

        ds.PatientID = norm_string(
            '{0}.{1}'.format(str(CONFIG.get('diseases', '')), rand_uid), 16)

        ds.PatientName = norm_string(
            fake_name, 16)

        ds.AccessionNumber = fake_acc_number

        ds.StudyDate = cur_date
        ds.StudyTime = cur_time
        ds.SeriesDate = cur_date
        ds.SeriesTime = cur_time

        try:
            ds.save_as(full_fn_fake)
            sync_send_file(full_fn_fake)
        except Exception as e:
            logging.error('errormsg: failed to save file [{0}]'.format(full_fn_fake))
            continue


def prepare_config(argv):
    global CONFIG
    try:
        opts, args = getopt.getopt(argv, "h",
                                   ["aet=", "ip=", "port=", "keyword=", "dicomfolder=", "diseases=",
                                    "end="])
        for opt, arg in opts:
            if opt == '-h':
                logging.info(
                    '--aet <aetitle> --ip <ip> --port <port> --keyword <keyword> --dicomfolder <dicomfolder>  --diseases <diseases> --end <end>')
                sys.exit()
            elif opt in ("--aet"):
                CONFIG["server"]["aet"] = arg
            elif opt in ("--ip"):
                CONFIG["server"]["ip"] = arg
            elif opt in ("--port"):
                CONFIG["server"]["port"] = arg
            elif opt in ("--keyword"):
                CONFIG["keyword"] = arg
            elif opt in ("--dicomfolder"):
                CONFIG["dicomfolder"] = arg
            elif opt in ("--diseases"):
                diseases = arg
                CONFIG["diseases"] = diseases
            elif opt in ("--end"):
                CONFIG["end"] = arg
    except Exception as e:
        logging.error("error: failed to get args", e)
    return True


if __name__ == '__main__':
    ospid = os.getpid()
    if not prepare_config(sys.argv[1:]):
        logging.info("failed to start")
        sys.exit(0)

    src_folder = CONFIG.get('dicomfolder', '')

    while src_folder[-1] == '/':
        src_folder = src_folder[0:-1]

    start = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    loop = 1
    while str(start) < str(CONFIG["end"]):
        folder_fake = "{0}/{1}{2}".format(log_path,
                                          str(CONFIG.get('keyword', '')) + '_' + str(CONFIG.get('diseases', '')),
                                          str(loop))
        fake_folder(
            folder=src_folder,
            folder_fake=folder_fake
        )
        loop = loop + 1
        start = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        del folder_fake
        gc.collect()


