# coding=utf-8
import logging
import threading
import os, shutil
import pydicom
import logging
import subprocess as sp
import time, datetime
import random
import math
import socket
import requests
import time
import queue

import threading

from ..common.dds_detect import *
from ..common.deletepatients import *
from ..common.duration_verify import *
from ..serializers import duration_record_Serializer

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


class DurationThread(threading.Thread):
    def __init__(self, *args, **kwargs):
        threading.Thread.__init__(self)
        self.Flag = True  # 停止标志位
        self.count = 0  # 可用来被外部访问的
        self.obj = duration.objects.get(id=kwargs["id"])
        self.sleepcount = self.obj.sleepcount if self.obj.sleepcount is not None else 9999
        self.sleeptime = self.obj.sleeptime if self.obj.sleeptime is not None else 0
        self.patientid = self.obj.patientid if self.obj.patientid is not None else '_'
        self.patientname = self.obj.patientname if self.obj.patientname is not None else '_'
        self.keyword = str(self.patientname) + str(self.patientid) + str(kwargs["id"])
        self.server = self.obj.Host.host
        self.q = queue.Queue()
        self.thread_num = 4
        self.durationdata ={}

        # 获取计算机名称
        if socket.gethostname() == "biomindqa38":
            self.local_aet = 'QA38'
        else:
            self.local_aet = 'QA120'
        self.full_fn_fake = '{0}/{1}'.format(settings.LOG_PATH, self.keyword)
        if not os.path.exists(self.full_fn_fake):
            os.makedirs(self.full_fn_fake)

    # 匿名数据队列
    def run(self):
        filecount = 1
        dicomobj = dicom.objects.filter(fileid__in=self.obj.dicom.split(","))
        try:
            file_end = int(self.obj.sendcount)
            while True:
                if filecount > file_end:
                    break
                if file_end >= filecount > int(dicomobj.count()):
                    dicomobj = dicom.objects.filter(fileid__in=self.obj.dicom.split(","))
                for j in dicomobj:
                    if filecount > file_end:
                        break
                    else:
                        src_folder = str(j.route)
                        while src_folder[-1] == '/':
                            src_folder = src_folder[0:-1]
                        self.q.put([src_folder, j.diseases])
                    filecount = filecount + 1
            logger.info("ID:{0} --- 队列:{1}".format(self.obj.id, self.q))
            self.obj.sendstatus = True
            self.obj.save()

            threads = []
            for i in range(self.thread_num):
                t = threading.Thread(target=self.durationAnony, args=(self.q,))
                # args需要输出的是一个元组，如果只有一个参数，后面加，表示元组，否则会报错
                threads.append(t)
            for i in range(self.thread_num):
                threads[i].start()
            for i in range(self.thread_num):
                threads[i].join()
        except Exception as e:
            logger.error("队列生成失败：{0}".format(e))

    def durationStop(self):
        # 改变状态
        self.obj.sendstatus = False
        self.obj.save()
        drobj = duration_record.objects.filter(Duration=self.id, imagecount=None)
        # 删除错误数据
        for j in drobj:
            delete_patients_duration(j.studyinstanceuid, self.obj.Host.id, "studyinstanceuid", False)
        drobj.delete()
        # 删除 文件夹
        folder = "/home/biomind/Biomind_Test_Platform/logs/{0}{1}{2}".format(str(self.obj.patientname),
                                                                             str(self.obj.patientid),
                                                                             str(self.id))
        if os.path.exists(folder):
            shutil.rmtree(folder)

    def durationAnony(self, q):
        study_fakeinfos = {}
        while True:
            if q.empty():
                return
            else:
                try:
                    logger.info("队列开始{}".format(q.get()))
                    self.folder_ergodic(folder=q.get()[0], diseases=q.get()[1],
                                        study_fakeinfos=study_fakeinfos)
                except Exception as e:
                    logging.error('folder_ergodic error: {0}'.format(e))

    def connect_influx(self):
        requests.post('http://192.168.1.121:8086/write?db=auto_test', data=self.durationdata)

    def get_fake_name(self, rand_uid, fake_prefix):
        ts = time.localtime(time.time())
        return "{0}{1}{2}".format(fake_prefix, time.strftime("%m%d", ts), self.norm_string(rand_uid, 6))

    def sync_send_file(self, file_name, commands):

        # 发送数据
        try:
            logger.info("发送开始{}")
            starttime = time.time()
            popen = sp.Popen(commands, stderr=sp.PIPE, stdout=sp.PIPE, shell=False)
            popen.communicate()
            endtime = time.time()
            self.durationdata['time'] = str('%.2f' % (float(endtime - starttime)))
            self.durationdata['sendtime'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(starttime))
            self.durationdata['endtime'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(endtime))
            os.remove(file_name)
        except Exception as e:
            logging.error('send_file error: {0}'.format(e))

    def norm_string(self, str, len_norm):
        str_dest = str
        while len(str_dest) > len_norm or str_dest[0] == '.':
            str_dest = str_dest[1:]
        return str_dest

    def get_fake_accession_number(self, acc_number, rand_uid):
        str = "{0}_{1}".format(acc_number, rand_uid)
        return self.norm_string(str, 16)

    def get_study_fakeinfo(self, studyuid, acc_number, study_fakeinfos):
        if not study_fakeinfos.get(studyuid):
            rand_uid = get_rand_uid()
            # "fake_name": get_fake_name(rand_uid, keyword),
            info = {
                "rand_uid": rand_uid,
                "fake_acc_num": self.get_fake_accession_number(acc_number, rand_uid),
                "cur_date": get_date(),
                "cur_time": get_time()
            }
            study_fakeinfos[studyuid] = info
        fake_info = study_fakeinfos[studyuid]
        logging.info("---debug{}".format(fake_info))
        return fake_info

    # 判断是否 同一个 Series
    def delayed(self, study_fakeinfos):
        SeriesInstanceUID = {}
        if study_fakeinfos["count"] == int(self.sleepcount):
            time.sleep(int(self.sleeptime))
            study_fakeinfos["count"] = 0
        if not SeriesInstanceUID.get(self.SeriesInstanceUID) and self.obj.series is True:
            time.sleep(int(self.sleeptime))
            SeriesInstanceUID[self.SeriesInstanceUID] = 1

    # 匿名数据
    def anonymization(self, full_fn, full_fn_fake, diseases, study_fakeinfos):
        logger.info("匿名开始{}")
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
            study_fakeinfo = self.get_study_fakeinfo(study_uid, acc_number, study_fakeinfos)
            rand_uid = study_fakeinfo.get("rand_uid")
            fake_acc_number = study_fakeinfo.get("fake_acc_num")
            cur_date = study_fakeinfo.get("cur_date")
            cur_time = study_fakeinfo.get("cur_time")
        except Exception as e:
            logging.error(
                'failed to fake studyinstanceuid: file[{0}], error[{1}]'.format(full_fn, e))
        ds.StudyInstanceUID = self.norm_string(
            '{0}.{1}'.format(study_uid, rand_uid), 64)
        try:
            series_uid = ds.SeriesInstanceUID
        except Exception as e:
            logging.error(
                'failed to fake seriesinstanceuid: file[{0}], error[{1}]'.format(full_fn, e))
        ds.SeriesInstanceUID = self.norm_string(
            '{0}.{1}'.format(series_uid, rand_uid), 64)
        self.SeriesInstanceUID = ds.SeriesInstanceUID
        instance_uid = ''
        try:
            instance_uid = ds.SOPInstanceUID
        except Exception as e:
            logging.error(
                'failed to fake sopinstanceuid: file[{0}], error[{1}]'.format(full_fn, e))
        ds.SOPInstanceUID = self.norm_string(
            '{0}.{1}'.format(instance_uid, rand_uid), 64)
        ds.PatientID = self.norm_string(
            '{0}{1}{2}'.format(str(diseases), self.patientid, rand_uid), 24)

        ds.PatientName = self.norm_string(
            '{0}{1}{2}'.format(str(diseases), self.patientname, rand_uid), 24)
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
        try:
            if not study_fakeinfos.get(ds.StudyInstanceUID):
                if self.durationdata != {}:
                    try:
                        logger.info(self.durationdata)
                        duration_record.objects.create(**self.durationdata)
                    except Exception as e:
                        logger.error('更新数据库失败： [{0}][{1}]'.format(self.durationdata, e))

                create_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
                self.durationdata = {
                    "patientid": ds.PatientID,
                    "patientname": ds.PatientName,
                    "accessionnumber": ds.AccessionNumber,
                    "studyinstanceuid": ds.StudyInstanceUID,
                    "studyolduid": studyolduid,
                    "imagecount": 1,
                    "sendserver": self.server,
                    "duration_id": self.obj.id,
                    "update_time": create_time,
                    "create_time": create_time
                }
            else:
                self.durationdata["imagecount"] = int(self.durationdata["imagecount"]) + 1
        except Exception as e:
            logger.error('获取数据失败： [{0}][{1}]'.format(self.durationdata, e))

    # 遍历文件夹
    def folder_ergodic(self, folder, diseases, study_fakeinfos):
        logger.info("遍历开始{}")
        file_names = os.listdir(folder)
        file_names.sort()

        for fn in file_names:
            full_fn = os.path.join(folder, fn)
            full_fn_fake = os.path.join(self.full_fn_fake, fn)
            if (os.path.splitext(fn)[1] in ['.dcm'] == False):
                continue
            elif (os.path.isdir(full_fn)):
                self.folder_ergodic(folder=full_fn, diseases=diseases, study_fakeinfos=study_fakeinfos)
                continue
            try:
                self.anonymization(full_fn, full_fn_fake, diseases, study_fakeinfos)
            except Exception as e:
                logging.error("匿名错误 {}".format(e))
                continue
            try:
                commands = [
                    "storescu",
                    self.obj.Host.host,
                    self.obj.port,
                    "-aec", self.obj.Host.remarks,
                    "-aet", self.local_aet,
                    full_fn_fake
                ]
                self.sync_send_file(full_fn_fake, commands)
            except Exception as e:
                logging.error('errormsg: failed to sync_send [{0}]'.format(full_fn_fake))
                continue
            try:
                study_fakeinfos["count"] = int(study_fakeinfos["count"]) + 1
                self.delayed(study_fakeinfos)
            except Exception as e:
                logging.error('errormsg: failed delayed{0}]'.format(full_fn_fake))
                continue

    def setFlag(self, parm):  # 外部停止线程的操作函数
        self.Flag = parm  # boolean

    def setParm(self, parm):  # 外部修改内部信息函数
        self.Parm = parm

    def getParm(self):  # 外部获得内部信息函数
        return self.parm
