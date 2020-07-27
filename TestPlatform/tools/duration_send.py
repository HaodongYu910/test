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
from TestPlatform.serializers import duration_record_Deserializer, duration_record_Serializer
logger = logging.getLogger(__name__)  # 这里使用 __name__ 动态搜索定义的 logger 配置。

# 下面只是个数据结构示例，具体的值会采用命令行传进来的
CONFIG = {
    'local': {
        'aet': 'ORTHANC208'
    },
    'server': {
        'aet': 'ORTHANC',
        'ip': '192.168.1.208',
        'port': '4242'
    },
    'keyword': 'duration',
    'dicomfolder': '/home/biomind/testDatas'
}


def insertDB(data):
    conn = pymysql.connect(host='192.168.2.38', user='root', passwd='P@ssw0rd2o8', db='test',
                           charset="utf8");  # 连接数据库
    cur = conn.cursor()
    try:
        cur.execute(
            'INSERT INTO duration_record values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',
            data)
        conn.commit()
    except:
        conn.rollback()
    cur.close()
    conn.close()
    return data


def get_date():
    localtime = time.localtime(time.time())
    return (time.strftime("%Y-%m-%d", localtime))


def get_time():
    localtime = time.localtime(time.time())
    return (time.strftime("%H:%M:%S", localtime))


def get_rand_uid():
    rand_val = random.randint(1, math.pow(10, 8) - 1)
    return "%08d" % rand_val


def get_fake_name(rand_uid):
    fake_prefix = CONFIG["keyword"]
    return "{0}{1}".format(fake_prefix, rand_uid)


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


def sync_send(folder):
    if not folder or not os.path.exists(folder):
        logging.info('send: path is not exist [{0}]'.format(folder))
        return

    file_names = os.listdir(folder)
    file_names.sort()

    logging.info(' sending: {0}'.format(folder))
    for fn in tqdm(file_names):
        full_fn = os.path.join(folder, fn)

        if (fn == '.DS_Store'):
            continue
        elif (os.path.isdir(full_fn)):
            sync_send(full_fn)
            continue
        try:
            sync_send_file(full_fn)
        except Exception as e:
            logging.error(
                'failed to send file: file[{0}], error[{1}]'.format(full_fn, e))
            continue


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


def add_image(sendtime, study_infos, study_uid, patientid, accessionnumber):

    if study_infos.get(study_uid):
        study_infos[study_uid]["imagecount"] = study_infos[study_uid]["imagecount"] + 1
    else:
        study_info = {
            "sendtime": sendtime,
            "accessionnumber": accessionnumber,
            "patientid": patientid,
            "imagecount": 1
        }
        study_infos[study_uid] = study_info


def fake_folder(folder, folder_fake, study_fakeinfos, study_infos):
    if not os.path.exists(folder_fake):
        os.makedirs(folder_fake)

    file_names = os.listdir(folder)
    file_names.sort()

    for fn in tqdm(file_names):
        full_fn = os.path.join(folder, fn)
        full_fn_fake = os.path.join(folder_fake, fn)

        if (fn == '.DS_Store'):
            continue
        elif (os.path.isdir(full_fn)):
            fake_folder(full_fn, full_fn_fake, study_fakeinfos, study_infos)
            continue
        try:
            ds = pydicom.dcmread(full_fn, force=True)
        except Exception as e:
            logging.error('errormsg: failed to read file [{0}]'.format(full_fn))
            continue

        study_uid = ''
        try:
            study_uid = ds.StudyInstanceUID
            acc_number = ds.AccessionNumber
            study_fakeinfo = get_study_fakeinfo(study_uid, acc_number, study_fakeinfos)
            rand_uid = study_fakeinfo.get("rand_uid")
            fake_name = study_fakeinfo.get("fake_name")
            fake_acc_number = study_fakeinfo.get("fake_acc_num")
            cur_date = study_fakeinfo.get("cur_date")
            cur_time = study_fakeinfo.get("cur_time")
        except Exception as e:
            logging.info(
                'failed to fake studyinstanceuid: file[{0}], error[{1}]'.format(full_fn, e))
            continue
        ds.StudyInstanceUID = norm_string(
            '{0}.{1}'.format(study_uid, rand_uid), 64)

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

        ds.PatientID = norm_string(
            fake_name, 16)

        ds.PatientName = norm_string(
            fake_name, 16)

        ds.AccessionNumber = fake_acc_number

        ds.StudyDate = cur_date
        ds.StudyTime = cur_time
        ds.SeriesDate = cur_date
        ds.SeriesTime = cur_time
        # ds.ContentDate = cur_date
        # ds.ContentTime = cur_time
        # ds.AcquisitionDate = cur_date
        # ds.AcquisitionTime = cur_time

        send_time = ds.StudyDate + "-" + ds.StudyTime

        try:
            ds.save_as(full_fn_fake)
            new_study_uid = ds.StudyInstanceUID
            new_patient_id = ds.PatientID

            add_image(
                sendtime=send_time,
                study_infos=study_infos,
                study_uid=new_study_uid,
                patientid=new_patient_id,
                accessionnumber=ds.AccessionNumber
            )

        except Exception as e:
            logging.error('errormsg: failed to save file [{0}]'.format(full_fn_fake))
            continue


def prepare_config(server_ip,server_port,server_aet,keyword,dicom):
    global CONFIG
    try:
        CONFIG["server"]["aet"] = server_aet
        CONFIG["server"]["ip"] = server_ip
        CONFIG["server"]["port"] = server_port
        keyword = norm_string(keyword, 8)
        if dicom == 'All':
            dicomfolder = '/home/biomind/testDatas'
        else:
            dicomfolder = '/home/biomind/testDatas/'+str(dicom)
            keyword = keyword + dicom

        CONFIG["keyword"] = keyword
        CONFIG["dicomfolder"] = dicomfolder
    except Exception as e:
        logging.error("error: failed to get args")


    logging.info("please check config, waiting for 5 seconds...")
    time.sleep(5)
    logging.basicConfig(filemode='a+',
                        format="%(asctime)s [%(funcName)s:%(lineno)s] %(levelname)s: %(message)s",
                        datefmt="%Y-%m-%d %H:%M:%S", level=logging.DEBUG)
    return True



def stress_duration(server_ip,server_port,server_aet,keyword,dicom,end_time):
    log_path ='/home/biomind/Biomind_Test_Platform/logs'
    prepare_config(server_ip,server_port,server_aet,keyword,dicom)
    folder = CONFIG.get('dicomfolder', '')
    logging.info('start to send: path[{0}]'.format(folder))

    src_folder = folder
    while src_folder[-1] == '/':
        src_folder = src_folder[0:-1]

    loop_times = 0

    while datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")!=end_time:
        loop_times = loop_times + 1
        folder_fake = "{0}/{1}{2}".format(log_path,CONFIG.get('keyword', ''),loop_times)

        study_fakeinfos = {}
        study_infos = {}

        fake_folder(
            folder=src_folder,
            folder_fake=folder_fake,
            study_fakeinfos=study_fakeinfos,
            study_infos=study_infos
        )

        for (k, v) in study_infos.items():
            v['studyinstanceuid']=k
            stressserializer = duration_record_Serializer(data=v)
            with transaction.atomic():
                stressserializer.is_valid()
                stressserializer.save()

        time.sleep(1)
        sync_send(folder_fake)
        shutil.rmtree(folder_fake)

