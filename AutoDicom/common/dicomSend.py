# coding=utf-8
'''
作用：
把文件夹中的所有study，匿名成不同的uid，持续发到storescp中。
参数说明：
1，CONFIG.local：本storescu的信息，包括ae title
2，CONFIG.server：storescp的信息，包括ae title、ip、port
3，CONFIG.keyword：发送文件匿名tags（patientID, patientName）的前缀关键词
4，CONFIG.folderid：需要发送dicom文件的所在目录id
'''

import os, shutil
import sys, getopt
import pydicom
import logging
import subprocess as sp
import time, datetime
import random
import math
import pymysql
import socket


# import requests
#
#
# # 链接InfluxDB时序数据库
#
# def connect_influx(data):
#     posturl = 'http://127.0.0.1:8086/write?db=autotest'
#     requests.post(posturl, data=data)

# 链接mysql数据库
def sqlDB(sql, data, type):
    conn = pymysql.connect(host='192.168.1.121', user='root', passwd='P@ssw0rd2o8', db='auto_test',
                           charset="utf8");  # 连接数据库
    cur = conn.cursor()
    if type == 'select':
        try:
            # 查询数据
            cr = cur.execute(sql)  # 查询
            data = cur.fetchmany(cr)
            conn.commit()
        except Exception as e:
            conn.rollback()
    else:
        try:
            logging.info("sql:{0},data:{1}".format(sql, data))
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
    rand_val = random.randint(1, math.pow(10, 16) - 1)
    return "%08d" % rand_val


def get_fake_name(rand_uid, fake_prefix):
    ts = time.localtime(time.time())
    return "{0}{1}{2}".format(fake_prefix, time.strftime("%m%d", ts), norm_string(rand_uid, 6))


def sync_send_file(file_name, commands):
    # 发送数据
    try:
        starttime = time.time()
        popen = sp.Popen(commands, stderr=sp.PIPE, stdout=sp.PIPE, shell=False)
        popen.communicate()
        endtime = time.time()
        diff = str('%.2f' % (float(endtime - starttime)))
        start = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(starttime))
        end = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(endtime))
        os.remove(file_name)
    except Exception as e:
        logging.error('send_file error: {0}'.format(e))
    return start, end, diff


def norm_string(str, len_norm):
    str_dest = str
    while len(str_dest) > len_norm or str_dest[0] == '.':
        str_dest = str_dest[1:]
    return str_dest


def get_fake_accession_number(acc_number, rand_uid):
    str = "{0}_{1}".format(acc_number, rand_uid)
    return norm_string(str, 16)


def get_study_fakeinfo(studyuid, acc_number, study_fakeinfos):
    if not study_fakeinfos.get(studyuid):
        rand_uid = get_rand_uid()
        # "fake_name": get_fake_name(rand_uid, keyword),
        info = {
            "rand_uid": rand_uid,
            "fake_acc_num": get_fake_accession_number(acc_number, rand_uid),
            "cur_date": get_date(),
            "cur_time": get_time()
        }
        study_fakeinfos[studyuid] = info
    fake_info = study_fakeinfos[studyuid]
    logging.info("---debug{}".format(fake_info))
    return fake_info


# 判断是否 同一个 Series
def delayed(Seriesinstanceuid, image, CONFIG):
    if image["count"] == int(CONFIG.get('sleepcount', '')):
        time.sleep(int(CONFIG.get('sleeptime', '')))
        image["count"] = 0
    if CONFIG.get('Seriesinstanceuid', '') != Seriesinstanceuid and CONFIG.get('Series', '') == '1':
        time.sleep(int(CONFIG.get('sleeptime', '')))
        CONFIG["Seriesinstanceuid"] = Seriesinstanceuid


# 保存发送记录
def add_record(study_infos, study_uid, sqldata, ):
    try:
        if study_infos.get(study_uid):
            study_infos[study_uid] = study_infos[study_uid] + 1
        else:
            study_infos[study_uid] = 1
            try:
                sqlDB(sqldata, [], 'INSERT')
            except Exception as e:
                logging.error("更新mysql失败：{0}".format(e))
    except Exception as e:
        logging.error('errormsg: failed to sql [{0}]'.format(e))


# 匿名数据
def anonymization(full_fn, full_fn_fake, diseases, CONFIG):
    study_uid = ''
    series_uid = ''
    try:
        ds = pydicom.dcmread(full_fn, force=True)
    except Exception as e:
        logging.error('errormsg: failed to read file [{0}]'.format(full_fn))
    try:
        study_uid = ds.StudyInstanceUID
        studyolduid = ds.StudyInstanceUID
        Seriesinstanceuid = ds.SeriesInstanceUID
        acc_number = ds.AccessionNumber
        study_fakeinfo = get_study_fakeinfo(study_uid, acc_number, study_fakeinfos)
        rand_uid = study_fakeinfo.get("rand_uid")
        fake_acc_number = study_fakeinfo.get("fake_acc_num")
        cur_date = study_fakeinfo.get("cur_date")
        cur_time = study_fakeinfo.get("cur_time")
    except Exception as e:
        logging.error(
            'failed to fake studyinstanceuid: file[{0}], error[{1}]'.format(full_fn, e))
    ds.StudyInstanceUID = norm_string(
        '{0}.{1}'.format(study_uid, rand_uid), 64)
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
        logging.error(
            'failed to fake sopinstanceuid: file[{0}], error[{1}]'.format(full_fn, e))
    ds.SOPInstanceUID = norm_string(
        '{0}.{1}'.format(instance_uid, rand_uid), 64)
    ds.PatientID = norm_string(
        '{0}{1}{2}'.format(str(diseases), str(CONFIG["patientid"]), rand_uid), 24)

    ds.PatientName = norm_string(
        '{0}{1}{2}'.format(str(diseases), str(CONFIG["patientname"]), rand_uid), 24)
    ds.AccessionNumber = fake_acc_number

    ds.StudyDate = cur_date
    ds.StudyTime = cur_time
    ds.SeriesDate = cur_date
    ds.SeriesTime = cur_time
    # ds.ContentDate = cur_date
    # ds.ContentTime = cur_time
    # ds.AcquisitionDate = cur_date
    # ds.AcquisitionTime = cur_time

    # send_time = ds.StudyDate + "-" + ds.StudyTime
    try:
        ds.save_as(full_fn_fake)
    except Exception as e:
        logging.error('errormsg: failed to save file [{0}]'.format(full_fn_fake))
    logging.info("ds.StudyInstanceUID:{}".format(ds.StudyInstanceUID))
    logging.info("ds.PatientID:{0}".format(ds.PatientID))
    logging.info("ds.PatientName:{0}".format(ds.PatientName))
    logging.info("ds.AccessionNumber:{0}".format(ds.AccessionNumber))
    logging.info("ds.studyolduid:{0}".format(studyolduid))
    logging.info("ds.Seriesinstanceuid:{0}".format(Seriesinstanceuid))
    return ds.StudyInstanceUID, ds.PatientID, ds.PatientName, studyolduid, ds.AccessionNumber, Seriesinstanceuid


# 遍历文件夹
def fake_folder(folder, folder_fake, study_fakeinfos, study_infos, image, diseases, CONFIG):
    if not os.path.exists(folder_fake):
        os.makedirs(folder_fake)
    file_names = os.listdir(folder)
    file_names.sort()

    for fn in file_names:
        full_fn = os.path.join(folder, fn)
        full_fn_fake = os.path.join(folder_fake, fn)

        if (os.path.splitext(fn)[1] in ['.dcm'] == False):
            continue
        elif (os.path.isdir(full_fn)):
            fake_folder(full_fn, full_fn_fake, study_fakeinfos, study_infos, image, diseases, CONFIG)
            continue
        try:
            newstudyuid, newpatientid, newpatientname, studyolduid, accessionNumber, Seriesinstanceuid = anonymization(
                full_fn, full_fn_fake, diseases, CONFIG)
        except Exception as e:
            logging.error("匿名错误 {}".format(e))
            continue
        try:
            commands = [
                "storescu",
                CONFIG["ip"],
                CONFIG["port"],
                "-aec", CONFIG["aet"],
                "-aet", CONFIG["local_aet"],
                full_fn_fake
            ]
            start, end, diff = sync_send_file(full_fn_fake, commands)
        except Exception as e:
            logging.error('errormsg: failed to sync_send [{0}]'.format(full_fn_fake))
            continue
        try:
            sqldata = "INSERT INTO duration_record values(NULL,\'{0}\', \'{1}\', \'{2}\', \'{3}\', \'{4}\', NULL, NULL,NULL, NULL,\'{5}\',\'{6}\', \'{7}\', \'{8}\',\'{9}\', \'{10}\',\'{11}\',\'{12}\', NULL,NULL,NULL,NULL)".format(
                newpatientid, newpatientname, accessionNumber, newstudyuid, studyolduid, CONFIG['ip'], start,
                start, diff, int(CONFIG.get('durationid', '')), start, end, diseases)

            add_record(
                study_infos=study_infos,
                study_uid=newstudyuid,
                sqldata=sqldata
            )
        except Exception as e:
            logging.error('errormsg: failed to save_send_record file [{0}][[1]]'.format(full_fn, e))
            continue
        try:
            image["count"] = int(image["count"]) + 1
            delayed(Seriesinstanceuid, image, CONFIG)
        except Exception as e:
            logging.error('errormsg: failed delayed{0}]'.format(full_fn_fake))
            continue


#  参数
def prepare_config(argv):
    CONFIG = {}
    try:
        opts, args = getopt.getopt(argv, "h",
                                   ["aet=", "ip=", "port=", "patientid=", "patientname=", "folderid=", "durationid=",
                                    "end=", "sleepcount=", "sleeptime=", "series="])
        for opt, arg in opts:
            if opt == '-h':
                logging.info(
                    '--aet <aetitle> --ip <ip> --port <port> --patientid <patientid> --folderid <folderid>  --durationid <durationid>  --end <end>')
                sys.exit()
            elif opt in ("--aet"):
                CONFIG["aet"] = arg
            elif opt in ("--ip"):
                CONFIG["ip"] = arg
            elif opt in ("--port"):
                CONFIG["port"] = arg
            elif opt in ("--patientid"):
                CONFIG["patientid"] = arg
            elif opt in ("--patientname"):
                CONFIG["patientname"] = arg
            elif opt in ("--folderid"):
                CONFIG["folderid"] = arg
            elif opt in ("--durationid"):
                CONFIG["durationid"] = arg
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
    CONFIG["keyword"] = str(CONFIG["patientname"]) + str(CONFIG["patientid"]) + str(CONFIG["durationid"])
    log_path = "{0}/{1}".format('/home/biomind/Biomind_Test_Platform/logs', CONFIG["keyword"])
    if not os.path.exists(log_path):
        os.makedirs(log_path)

    log_file = '{0}/sendinfo.log'.format(log_path)
    logging.basicConfig(filename=log_file, filemode='a+',
                        format="%(asctime)s [%(funcName)s:%(lineno)s] %(levelname)s: %(message)s",
                        datefmt="%Y-%m-%d %H:%M:%S", level=logging.DEBUG)
    return CONFIG, log_path


# 修改影像数量
def ImageUpdate(study_infos):
    try:
        for k, v in study_infos.items():
            sql = 'UPDATE duration_record set imagecount =\'{0}\' where studyinstanceuid =\'{1}\''.format(v, k)
            sqlDB(sql, [], 'update')
        logging.info("发送成功{}".format(study_infos))
    except Exception as e:
        logging.error("更新影像张数失败studyinstanceuid：{0}，张数：{1}---错误{2}".format(k, v, e))


# 按照时间发送
def sendtime(sql, image, CONFIG):
    data = sqlDB(sql, [], 'select')
    count = 0
    start = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    while str(start) < str(CONFIG["end"]):
        if count > len(data):
            data = sqlDB(sql, [], 'select')
        for j in data:
            src_folder = str(j[0])
            while src_folder[-1] == '/':
                src_folder = src_folder[0:-1]
            folder_fake = "{0}/{1}{2}".format(log_path,
                                              str(CONFIG.get('keyword', '')) + '_' + str(j[1]),
                                              str(count))
            study_fakeinfos = {}
            study_infos = {}
            study_infos["count"] = 0
            fake_folder(
                folder=src_folder,
                folder_fake=folder_fake,
                study_fakeinfos=study_fakeinfos,
                study_infos=study_infos,
                image=image,
                diseases=j[1],
                CONFIG=CONFIG
            )
            ImageUpdate(study_infos)
            start = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


if __name__ == '__main__':
    try:
        image = {}
        image["count"] = 0
        count = 1
        # 获取进程ID
        ospid = os.getpid()
        CONFIG, log_path = prepare_config(sys.argv[1:])
        # 查询发送数据sql
        if str(CONFIG["sleepcount"]) == '8787':
            sql = "select route,diseases from dicom  where predictor in ({0}) and stressstatus in (1,2)".format(
                CONFIG["folderid"])
        else:
            sql = "SELECT route,diseases FROM dicom where fileid ={0} and status = TRUE".format(CONFIG["folderid"])
        # 获取local_aet名称
        if socket.gethostname() == "biomindqa38":
            CONFIG["local_aet"] = 'QA38'
        else:
            CONFIG["local_aet"] = 'QA120'
        folder_fake = "{0}/{1}".format(log_path, str(CONFIG.get('keyword', '')))
        # 添加 pid号
        sqlDB('INSERT INTO pid values(%s,%s,%s)', [None, ospid, CONFIG['durationid']], 'INSERT')
    except Exception as e:
        logging.error("failed to start:{}".format(e))
        sys.exit(0)
    # 按时间发送
    if len(str(CONFIG["end"])) > 10:
        sendtime(sql, image, CONFIG)
    # 按数量发送
    else:
        end = int(CONFIG["end"])
        data = sqlDB(sql, [], 'select')
        # 循环发送
        for i in range(end):
            if count <= end and count > len(data):
                data = sqlDB(sql, [], 'select')
            for j in data:
                if count > end:
                    break
                else:
                    src_folder = str(j[0])
                    while src_folder[-1] == '/':
                        src_folder = src_folder[0:-1]
                    study_fakeinfos = {}
                    study_infos = {}
                    fake_folder(
                        folder=src_folder,
                        folder_fake=folder_fake,
                        study_fakeinfos=study_fakeinfos,
                        study_infos=study_infos,
                        image=image,
                        diseases=j[1],
                        CONFIG=CONFIG
                    )
                    ImageUpdate(study_infos)
                    count = count + 1
            if count > end:
                break
        # 执行状态判断
        pid = sqlDB('select count(1) from pid where durationid ="{0}"'.format(CONFIG["durationid"]), [], 'select')
        if int(pid[0][0]) == 1:
            sqlDB('UPDATE duration set sendstatus = 0 where id ={0}'.format(CONFIG["durationid"]), [], 'update')
            sqlDB('DELETE from pid where pid ="{0}"'.format(ospid), [], 'DELETE')
            if os.path.exists(folder_fake):
                shutil.rmtree(folder_fake)
        else:
            sqlDB('DELETE from pid where pid ="{0}"'.format(ospid), [], 'DELETE')