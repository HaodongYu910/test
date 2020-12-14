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
import subprocess as sp
import time, datetime
import random
import math
import pymysql
import requests

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
    'dicomfolder': '/files/',
    'durationid': '1',
    'diseases': 'all',
    'start': 0,
    'end': 1,
    'sleepcount':9999,
    'sleeptime':1,
    'Seriesinstanceuid':'1',
    'series':'0'
}


# 链接InfluxDB时序数据库

def connect_to_influx(data):
    posturl = 'http://192.168.1.121:8086/write?db=autotest'
    requests.post(posturl, data=data)

# 链接mysql数据库
def sqlDB(sql, data):
    conn = pymysql.connect(host='192.168.1.121', user='root', passwd='P@ssw0rd2o8', db='autotest',
                           charset="utf8");  # 连接数据库
    cur = conn.cursor()
    try:
        logging.info(sql, data)
        cur.execute(sql, data)
        conn.commit()
    except Exception as e:
        conn.rollback()
    cur.close()
    conn.close()
    return data


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


def delayed(Seriesinstanceuid):
    if study_infos["count"] == int(CONFIG.get('sleepcount', '')):
        time.sleep(int(CONFIG.get('sleeptime', '')))
        study_infos["count"] = 0
    if CONFIG.get('Seriesinstanceuid', '') != Seriesinstanceuid and CONFIG.get('Series', '') == '1':
        time.sleep(int(CONFIG.get('sleeptime', '')))
        CONFIG["Seriesinstanceuid"] = Seriesinstanceuid

def add_image(study_infos, study_uid, patientid, accessionnumber,study_old_uid):
    studytime = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    try:
        if study_infos.get(study_uid):
            data = "duration,studyinstanceuid={0},duration_id={1} value=1".format(study_uid,CONFIG.get('durationid', ''))
            connect_to_influx(data)
        else:
            study_infos[study_uid] = study_uid
            sqlDB('INSERT INTO duration_record values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',
                  [None, patientid, accessionnumber, study_uid,study_old_uid,None, None,
                   None, None, CONFIG.get('server', {}).get('ip'),
                   studytime, CONFIG.get('durationid', ''),studytime , studytime])
    except Exception as e:
        logging.error('errormsg: failed to sql [{0}]'.format(e))


def fake_folder(folder, folder_fake, study_fakeinfos, study_infos):
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
        # ds.ContentDate = cur_date
        # ds.ContentTime = cur_time
        # ds.AcquisitionDate = cur_date
        # ds.AcquisitionTime = cur_time

        #send_time = ds.StudyDate + "-" + ds.StudyTime

        try:
            ds.save_as(full_fn_fake)
            new_study_uid = ds.StudyInstanceUID
            new_patient_id = ds.PatientID
        except Exception as e:
            logging.error('errormsg: failed to save file [{0}]'.format(full_fn_fake))
            continue
        try:
            study_infos["count"] = int(study_infos["count"]) + 1
            sync_send_file(full_fn_fake)
            add_image(
                study_infos=study_infos,
                study_uid=new_study_uid,
                patientid=new_patient_id,
                accessionnumber=ds.AccessionNumber,
                study_old_uid=study_old_uid
            )
            delayed(Seriesinstanceuid)
        except Exception as e:
            logging.error('errormsg: failed to sync_send file [{0}][[1]]'.format(full_fn,e))
            continue


def prepare_config(argv):
    global CONFIG
    try:
        opts, args = getopt.getopt(argv, "h",
                                   ["aet=", "ip=", "port=", "keyword=", "dicomfolder=", "durationid=", "diseases=",
                                    "start=", "end=","sleepcount=", "sleeptime=","series="])
        for opt, arg in opts:
            if opt == '-h':
                logging.info(
                    '--aet <aetitle> --ip <ip> --port <port> --keyword <keyword> --dicomfolder <dicomfolder>  --durationid <durationid> --diseases <diseases> --end <end>')
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
            elif opt in ("--durationid"):
                CONFIG["durationid"] = arg
            elif opt in ("--diseases"):
                diseases = arg
                CONFIG["diseases"] = diseases
            elif opt in ("--start"):
                CONFIG["start"] = arg
            elif opt in ("--end"):
                CONFIG["end"] = arg
            elif opt in ("--sleepcount"):
                CONFIG["sleepcount"] = arg
            elif opt in ("--sleeptime"):
                CONFIG["sleeptime"] = arg
            elif opt in ("--series"):
                CONFIG["series"] = arg

    except Exception as e:
        logging.error("error: failed to get args", e)

    keyword = CONFIG["keyword"]
    global log_path
    log_path = "{0}/{1}".format(log_path, keyword)
    if not os.path.exists(log_path):
        os.makedirs(log_path)

    log_file = '{0}/{1}Send.log'.format(log_path, CONFIG["keyword"])
    logging.basicConfig(filename=log_file, filemode='a+',
                        format="%(asctime)s [%(funcName)s:%(lineno)s] %(levelname)s: %(message)s",
                        datefmt="%Y-%m-%d %H:%M:%S", level=logging.DEBUG)

    return True


if __name__ == '__main__':
    ospid = os.getpid()
    if not prepare_config(sys.argv[1:]):
        logging.info("failed to start")
        sys.exit(0)
    # 添加 pid号
    sqlDB('INSERT INTO pid values(%s,%s,%s)', [None, ospid, CONFIG.get('durationid', '')])
    src_folder = CONFIG.get('dicomfolder', '')

    while src_folder[-1] == '/':
        src_folder = src_folder[0:-1]

    start = CONFIG["start"]
    while int(start) < int(CONFIG["end"]):
        folder_fake = "{0}/{1}{2}".format(log_path,
                                          str(CONFIG.get('keyword', '')) + '_' + str(CONFIG.get('diseases', '')),
                                          str(start))
        study_fakeinfos = {}
        study_infos = {}
        study_infos["count"]=0
        fake_folder(
            folder=src_folder,
            folder_fake=folder_fake,
            study_fakeinfos=study_fakeinfos,
            study_infos=study_infos
        )

        del folder_fake
        del study_infos
        del study_fakeinfos
        gc.collect()

        start = int(start) + 1


    sqlDB('DELETE from pid where pid ="%s"', [ospid])
