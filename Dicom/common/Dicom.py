# coding=utf-8
import logging
from TestPlatform.models import GlobalHost
import threading
import os, shutil
import pydicom
import logging
import subprocess as sp
import time, datetime
import random
import math

import socket
from TestPlatform.models import dicom, duration
from Stress.models import stress
from .deletepatients import delete_patients_duration

logger = logging.getLogger(__name__)  # 这里使用 __name__ 动态搜索定义的 logger 配置


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


def norm_string(str, len_norm):
    str_dest = str
    while len(str_dest) > len_norm or str_dest[0] == '.':
        str_dest = str_dest[1:]
    return str_dest


def get_fake_accession_number(acc_number, rand_uid):
    str = "{0}_{1}".format(acc_number, rand_uid)
    return norm_string(str, 16)


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
    def get_study_fakeinfo(self,studyuid, acc_number, study_fakeinfos):
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

#
#     # 匿名数据
#     def anonymization(full_fn, full_fn_fake, diseases, CONFIG):
#         study_uid = ''
#         series_uid = ''
#         try:
#             ds = pydicom.dcmread(full_fn, force=True)
#         except Exception as e:
#             logging.error('errormsg: failed to read file [{0}]'.format(full_fn))
#         try:
#             study_uid = ds.StudyInstanceUID
#             studyolduid = ds.StudyInstanceUID
#             Seriesinstanceuid = ds.SeriesInstanceUID
#             acc_number = ds.AccessionNumber
#             study_fakeinfo = get_study_fakeinfo(study_uid, acc_number, study_fakeinfos)
#             rand_uid = study_fakeinfo.get("rand_uid")
#             fake_acc_number = study_fakeinfo.get("fake_acc_num")
#             cur_date = study_fakeinfo.get("cur_date")
#             cur_time = study_fakeinfo.get("cur_time")
#         except Exception as e:
#             logging.error(
#                 'failed to fake studyinstanceuid: file[{0}], error[{1}]'.format(full_fn, e))
#         ds.StudyInstanceUID = norm_string(
#             '{0}.{1}'.format(study_uid, rand_uid), 64)
#         try:
#             series_uid = ds.SeriesInstanceUID
#         except Exception as e:
#             logging.error(
#                 'failed to fake seriesinstanceuid: file[{0}], error[{1}]'.format(full_fn, e))
#         ds.SeriesInstanceUID = norm_string(
#             '{0}.{1}'.format(series_uid, rand_uid), 64)
#
#         instance_uid = ''
#         try:
#             instance_uid = ds.SOPInstanceUID
#         except Exception as e:
#             logging.error(
#                 'failed to fake sopinstanceuid: file[{0}], error[{1}]'.format(full_fn, e))
#         ds.SOPInstanceUID = norm_string(
#             '{0}.{1}'.format(instance_uid, rand_uid), 64)
#         ds.PatientID = norm_string(
#             '{0}{1}{2}'.format(str(diseases), str(CONFIG["patientid"]), rand_uid), 24)
#
#         ds.PatientName = norm_string(
#             '{0}{1}{2}'.format(str(diseases), str(CONFIG["patientname"]), rand_uid), 24)
#         ds.AccessionNumber = fake_acc_number
#
#         ds.StudyDate = cur_date
#         ds.StudyTime = cur_time
#         ds.SeriesDate = cur_date
#         ds.SeriesTime = cur_time
#         # ds.ContentDate = cur_date
#         # ds.ContentTime = cur_time
#         # ds.AcquisitionDate = cur_date
#         # ds.AcquisitionTime = cur_time
#
#         # send_time = ds.StudyDate + "-" + ds.StudyTime
#         try:
#             ds.save_as(full_fn_fake)
#         except Exception as e:
#             logging.error('errormsg: failed to save file [{0}]'.format(full_fn_fake))
#         return ds.StudyInstanceUID, ds.PatientID, ds.PatientName, studyolduid, ds.AccessionNumber, Seriesinstanceuid
#
#     # 遍历文件夹
#     def fake_folder(folder, folder_fake, study_fakeinfos, study_infos, image, diseases, CONFIG):
#         if not os.path.exists(folder_fake):
#             os.makedirs(folder_fake)
#         file_names = os.listdir(folder)
#         file_names.sort()
#
#         for fn in file_names:
#             full_fn = os.path.join(folder, fn)
#             full_fn_fake = os.path.join(folder_fake, fn)
#
#             if (os.path.splitext(fn)[1] in ['.dcm'] == False):
#                 continue
#             elif (os.path.isdir(full_fn)):
#                 fake_folder(full_fn, full_fn_fake, study_fakeinfos, study_infos, image, diseases, CONFIG)
#                 continue
#             try:
#                 newstudyuid, newpatientid, newpatientname, studyolduid, accessionNumber, Seriesinstanceuid = anonymization(
#                     full_fn, full_fn_fake, diseases, CONFIG)
#             except Exception as e:
#                 logging.error("匿名错误 {}".format(e))
#                 continue
#             try:
#                 commands = [
#                     "storescu",
#                     CONFIG["ip"],
#                     CONFIG["port"],
#                     "-aec", CONFIG["aet"],
#                     "-aet", CONFIG["local_aet"],
#                     full_fn_fake
#                 ]
#                 start, end, diff = sync_send_file(full_fn_fake, commands)
#             except Exception as e:
#                 logging.error('errormsg: failed to sync_send [{0}]'.format(full_fn_fake))
#                 continue
#             try:
#                 sqldata = "INSERT INTO duration_record values(NULL,\'{0}\', \'{1}\', \'{2}\', \'{3}\', NULL, NULL,NULL, NULL, \'{4}\',\'{5}\',\'{6}\', \'{7}\', \'{8}\',\'{9}\', \'{10}\',\'{11}\')".format(
#                     newpatientid, accessionNumber, newstudyuid, studyolduid, CONFIG['ip'], start,
#                     CONFIG.get('durationid', ''), start, start, end, diff, newpatientname)
#
#                 add_record(
#                     study_infos=study_infos,
#                     study_uid=newstudyuid,
#                     sqldata=sqldata
#                 )
#             except Exception as e:
#                 logging.error('errormsg: failed to save_send_record file [{0}][[1]]'.format(full_fn, e))
#                 continue
#             try:
#                 image["count"] = int(image["count"]) + 1
#                 delayed(Seriesinstanceuid, image, CONFIG)
#             except Exception as e:
#                 logging.error('errormsg: failed delayed{0}]'.format(full_fn_fake))
#                 continue
#
#
# class DicomThread(threading.Thread):
#     def __init__(self, *args, **kwargs):
#         threading.Thread.__init__(self)
#         self.Flag = True  # 停止标志位
#         # self.count = kwargs["count"]  # 可用来被外部访问的
#         #
#         self.type = kwargs["type"]
#         if kwargs["type"] == 'stress':
#             self.obj = stress.objects.get(stressid=kwargs["stressid"])
#             self.keyword = str(stress)+ str(kwargs["stressid"])
#
#         elif kwargs["type"] == 'duration':
#             self.obj = duration.objects.get(id=kwargs["id"])
#             self.keyword = str(self.obj.patientname) + str(self.obj.patientid) + str(kwargs["id"])
#         else:
#             self.stressid = kwargs["stressid"]
#         self.Hostobj = GlobalHost.objects.get(id=self.obj.hostid)
#         self.server = self.Hostobj.host
#
#         log_path = "/files/durationlog/{}".format(self.keyword)
#         if not os.path.exists(log_path):
#             os.makedirs(log_path)
#
#         log_file = '{0}/sendinfo.log'.format(log_path)
#         self.logging.basicConfig(filename=log_file, filemode='a+',
#                             format="%(asctime)s [%(funcName)s:%(lineno)s] %(levelname)s: %(message)s",
#                             datefmt="%Y-%m-%d %H:%M:%S", level=logging.DEBUG)
#
#
#     # 按照时间发送
#     def sendtime(self,sql, image, CONFIG):
#         data = sqlDB(sql, [], 'select')
#         count = 0
#         start = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#         while str(start) < str(CONFIG["end"]):
#             if count > len(data):
#                 data = sqlDB(sql, [], 'select')
#             for j in data:
#                 src_folder = str(j[0])
#                 while src_folder[-1] == '/':
#                     src_folder = src_folder[0:-1]
#                 folder_fake = "{0}/{1}{2}".format(log_path,
#                                                   str(CONFIG.get('keyword', '')) + '_' + str(j[1]),
#                                                   str(count))
#                 study_fakeinfos = {}
#                 study_infos = {}
#                 study_infos["count"] = 0
#                 fake_folder(
#                     folder=src_folder,
#                     folder_fake=folder_fake,
#                     study_fakeinfos=study_fakeinfos,
#                     study_infos=study_infos,
#                     image=image,
#                     diseases=j[1],
#                     CONFIG=CONFIG
#                 )
#                 ImageUpdate(study_infos)
#                 start = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#
#     # 正常发送
#     def normalSend(self,id):
#         obj = duration.objects.get(id=id)
#         for i in obj.dicom.split(","):
#             try:
#                 dicomobj = dicom.objects.filter(fileid=str(i), status=True)
#             except Exception as e:
#                 continue
#             for j in dicomobj:
#                 delete_patients_duration(j.studyinstanceuid, obj.hostid, 'StudyInstanceUID', False)
#             cmd = ('nohup /home/biomind/.local/share/virtualenvs/biomind-dvb8lGiB/bin/python3'
#                    ' /home/biomind/Biomind_Test_Platform/Dicom/common/dicomSend.py '
#                    '--ip {0} --aet {1} '
#                    '--port {2} '
#                    '--patientid {3} '
#                    '--patientname {4} '
#                    '--folderid {5} '
#                    '--durationid {6} '
#                    '--end {7} '
#                    '--sleepcount {8} '
#                    '--sleeptime {9} '
#                    '--series {10} &').format(obj.server, obj.aet, obj.port, 'patientid', 'patientname', i, id,
#                                              int(dicomobj.count()), 9999, 1, obj.series)
#
#             logger.info(cmd)
#             os.system(cmd)
#             time.sleep(1)
#
#         obj.sendstatus = True
#         obj.save()
#
#     # 按照数量发送
#     def sendcount(self,):
#          for i in range(self.end):
#             if count > len(data):
#                     data = sqlDB(sql, [], 'select')
#                 for j in data:
#                     src_folder = str(j[0])
#                     while src_folder[-1] == '/':
#                         src_folder = src_folder[0:-1]
#                     folder_fake = "{0}/{1}{2}".format(log_path,
#                                                       str(CONFIG.get('keyword', '')) + '_' + str(j[1]),
#                                                       str(count))
#                     study_fakeinfos = {}
#                     study_infos = {}
#                     study_infos["count"] = 0
#                     fake_folder(
#                         folder=src_folder,
#                         folder_fake=folder_fake,
#                         study_fakeinfos=study_fakeinfos,
#                         study_infos=study_infos,
#                         image=image,
#                         diseases=j[1],
#                         CONFIG=CONFIG
#                     )
#                     ImageUpdate(study_infos)
#                     start = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#
#     def setFlag(self, parm):  # 外部停止线程的操作函数
#         self.Flag = parm  # boolean
#
#     def setParm(self, parm):  # 外部修改内部信息函数
#         self.Parm = parm
#
#     def getParm(self):  # 外部获得内部信息函数
#         return self.parm
#

def sync_send_file(serverID, file_name):
    # 获取计算机名称
    if socket.gethostname() == "biomindqa38":
        local_aet = 'QA38'
    else:
        local_aet = 'QA120'
    Hostobj = GlobalHost.objects.get(id=serverID)
    # logging.info('send file: [{0}]'.format(file_name))
    commands = [
        "storescu",
        Hostobj.host,
        Hostobj.port,
        "-aec", Hostobj.description,
        "-aet", local_aet,
        file_name
    ]
    try:
        popen = sp.Popen(commands, stderr=sp.PIPE, stdout=sp.PIPE, shell=False)
        popen.communicate()
    except Exception as e:
        logger.error('send_file error: {0}'.format(e))


def fake_folder(serverID, folder):
    file_names = os.listdir(folder)
    file_names.sort()

    for fn in file_names:
        full_fn = os.path.join(folder, fn)

        if (os.path.splitext(fn)[1] in ['.dcm'] == False):
            continue
        elif (os.path.isdir(full_fn)):
            fake_folder(serverID, full_fn)
            continue
        try:
            sync_send_file(serverID, full_fn)
        except Exception as e:
            logging.error('errormsg: failed to sync_send file [{0}][[1]]'.format(full_fn, e))
            continue


def Send(serverID, route):
    try:
        src_folder = route
        while src_folder[-1] == '/':
            src_folder = src_folder[0:-1]
        fake_folder(serverID, src_folder)
    except Exception as e:
        logging.error("error: failed to send", e)
