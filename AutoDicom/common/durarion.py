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
from django.db import transaction
from django.conf import settings
import threading
from AutoDicom.models import duration_record, dicom, duration, dicom_group_detail
from ..common.deletepatients import delete_patients_duration
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


class DicomData(threading.Thread):
    def __init__(self, **kwargs):
        threading.Thread.__init__(self)
        self.Flag = True  # 停止标志位
        self.count = 1  # 可用来被外部访问
        self.files = kwargs["files"]
        self.end = kwargs["end"]

    # 匿名数据队列
    def run(self):
        q = queue.Queue()
        threads = []
        dicomObj = dicom.objects.filter(fileid__in=self.files)
        try:
            while True:
                if self.count > self.end:
                    break
                if self.end >= self.count > int(dicomObj.count()):
                    dicomObj = dicom.objects.filter(fileid__in=self.files)
                for j in dicomObj:
                    if self.count > self.end:
                        break
                    else:
                        src_folder = str(j.route)
                        while src_folder[-1] == '/':
                            src_folder = src_folder[0:-1]
                        q.put([src_folder, j.diseases, self.count])
                    self.count = self.count + 1

        except Exception as e:
            logger.error("队列数据生成失败：{0}".format(e))


class DurationThread(threading.Thread):
    def __init__(self, **kwargs):
        threading.Thread.__init__(self)
        self.Flag = True
        self.count = 0  # 可用来被外部访问
        self.obj = duration.objects.get(id=kwargs["id"])
        self.patientid = self.obj.patientid if self.obj.patientid is not None else '_'
        self.patientname = self.obj.patientname if self.obj.patientname is not None else '_'
        self.keyword = str(self.patientname) + str(self.patientid) + str(kwargs["id"])
        self.server = self.obj.Host.host
        self.thread_num = 4
        self.CountData = []
        self.SeriesInstanceUID = ''

        # 获取计算机名称
        if socket.gethostname() == "biomindqa38":
            self.local_aet = 'QA38'
        else:
            self.local_aet = 'QA120'
        self.full_fn_fake = '{0}/{1}'.format(settings.LOG_PATH, self.keyword)
        if not os.path.exists(self.full_fn_fake):
            os.makedirs(self.full_fn_fake)

    def anonymization(self, full_fn, full_fn_fake, info):
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
            rand_uid = str(info.get("rand_uid"))
            fake_acc_number = self.norm_string("{0}_{1}".format(acc_number, rand_uid), 16)
            cur_date = info.get("cur_date")
            cur_time = info.get("cur_time")
            diseases = info.get("diseases")
        except Exception as e:
            logging.error(
                'failed to fake: file[{0}], error[{1}]'.format(full_fn, e))
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
            logging.error('errormsg: failed to save file [{0}] --{1}'.format(full_fn_fake, e))
        return {
            "patientid": ds.PatientID,
            "patientname": ds.PatientName,
            "accessionnumber": ds.AccessionNumber,
            "studyinstanceuid": ds.StudyInstanceUID,
            "studyolduid": studyolduid,
            "sendserver": self.server,
            "diseases": diseases,
            "duration_id": self.obj.id
        }, Seriesinstanceuid

    def QueData(self):
        q = queue.Queue()
        filecount = 1
        dcmcount = 0
        dicomID = []
        # 查询 所以 dicom ID  优先组数据
        if self.obj.dicom is not None and len(self.obj.dicom.strip()) > 0:
            for i in dicom.objects.filter(fileid__in=self.obj.dicom.split(","), status=True):
                dicomID.append(i.id)
        if self.obj.group is not None and len(self.obj.group.strip()) > 0:
            for i in dicom_group_detail.objects.filter(group__id__in=self.obj.group.split(",")):
                dicomID.append(i.dicom_id)
        # 查询发送数据
        dicomObj = dicom.objects.filter(id__in=dicomID, status=True)
        try:
            file_end = int(self.obj.sendcount)
            while True:
                if filecount > file_end:
                    self.CountData.append(dcmcount)
                    break
                if file_end >= filecount > int(dicomObj.count()):
                    # 查询发送数据
                    dicomObj = dicom.objects.filter(id__in=dicomID, status=True)
                # 优先查询组
                for j in dicomObj:
                    self.CountData.append(dcmcount)
                    if filecount > file_end:
                        break
                    else:
                        src_folder = str(j.route)
                        while src_folder[-1] == '/':
                            src_folder = src_folder[0:-1]
                        try:
                            # "fake_name": get_fake_name(rand_uid, keyword),
                            info = {
                                "diseases": j.diseases,
                                "rand_uid": get_rand_uid(),
                                "cur_date": get_date(),
                                "cur_time": get_time()
                            }
                            file_names = os.listdir(src_folder)
                            file_names.sort()
                            for fn in file_names:
                                dcmcount = dcmcount + 1
                                full_fn = os.path.join(src_folder, fn)
                                full_fn_fake = os.path.join(self.full_fn_fake, '{0}{1}'.format(filecount, fn))
                                if (os.path.splitext(fn)[1] in ['.dcm'] == False):
                                    continue
                                try:
                                    q.put([full_fn, full_fn_fake, info, dcmcount])
                                except Exception as e:
                                    logging.error("[匿名错误]:{}".format(e))
                                    continue
                        except Exception as e:
                            logger.error("遍历文件：{}".format(e))
                    filecount = filecount + 1
            logger.info("self:{}".format(self.CountData))
            return q
        except Exception as e:
            logger.error("队列错误：{}".format(e))

    # 匿名数据队列
    def run(self):
        self.obj.sendstatus = True
        self.obj.save()
        q = self.QueData()
        threads = []

        try:
            for i in range(self.thread_num):
                t = threading.Thread(target=self.durationAnony, args=(q,))
                # args需要输出的是一个元组，如果只有一个参数，后面加，表示元组，否则会报错
                t.start()
                threads.append(t)
            for t in threads:
                t.join()
                time.sleep(1)
            # for i in range(self.thread_num):
            #     threads[i].start()
            # for i in range(self.thread_num):
            #     threads[i].join()
            self.obj.sendstatus = False
            self.obj.save()
        except Exception as e:
            logger.error("队列生成失败：{0}".format(e))

    def durationAnony(self, q):
        while not q.empty():
            if not os.path.exists(self.full_fn_fake):
                break
            self.count = self.count + 1
            testdata = q.get()
            full_fn_fake = testdata[1]
            try:
                data, Seriesinstanceuid = self.anonymization(testdata[0], full_fn_fake, testdata[2])
            except Exception as e:
                logger.error("匿名失败:{}".format(e))
            try:
                if testdata[3] in self.CountData:
                    create_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
                    data["update_time"] = create_time
                    data["create_time"] = create_time
                    duration_record.objects.create(**data)
            except Exception as e:
                logger.error('[获取数据失败]： [{0}]'.format(e))
            try:
                self.sync_send_file(full_fn_fake, data["studyinstanceuid"])
            except Exception as e:
                logging.error('errormsg: failed to sync_send [{0}]---报错：{1}'.format(q.get()[1], e))
                continue

            try:
                self.delayed(Seriesinstanceuid)
            except Exception as e:
                logger.error("delayed fail:{}".format(e))

    def connect_influx(self, data):
        try:
            influxdata = 'duration,durationid={0},studyuid="{1}",starttime="{2}",endtime="{3}",avgtime="{4}"'.format(
                self.obj.id, data["studyuid"], data["starttime"], data["endtime"], data["time"])
            requests.post('http://192.168.1.121:8086/write?db=auto_test', data=influxdata)
        except Exception as e:
            logger.error("保存connect_influx数据错误{}".format(e))

    def get_fake_name(self, rand_uid, fake_prefix):
        ts = time.localtime(time.time())
        return "{0}{1}{2}".format(fake_prefix, time.strftime("%m%d", ts), self.norm_string(rand_uid, 6))

    def sync_send_file(self, file_name, studyuid):
        # 发送数据
        try:
            commands = [
                "storescu",
                "-xs",  # 压缩方式
                self.obj.Host.host,
                self.obj.port,
                "-aec", self.obj.Host.remarks,
                "-aet", self.local_aet,
                file_name
            ]
            starttime = time.time()
            popen = sp.Popen(commands, stderr=sp.PIPE, stdout=sp.PIPE, shell=False)
            popen.communicate()
            endtime = time.time()
            self.connect_influx({'studyuid': studyuid,
                                 'time': str('%.2f' % (float(endtime - starttime))),
                                 'starttime': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(starttime)),
                                 'endtime': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(endtime))

                                 })
            os.remove(file_name)
        except Exception as e:
            logging.error('send_file error: {0}'.format(e))

    def norm_string(self, str, len_norm):
        str_dest = str
        while len(str_dest) > len_norm or str_dest[0] == '.':
            str_dest = str_dest[1:]
        return str_dest

    # 判断是否 同一个 Series
    def delayed(self, SeriesID):
        try:
            if self.obj.sleepcount is not None and int(self.obj.sleepcount) != 0 and self.obj.sleeptime is not None:
                imod = divmod(int(self.count), int(self.obj.sleepcount))
                if imod[1] == 0:
                    time.sleep(int(self.obj.sleeptime))
            if self.obj.series is True and self.obj.sleeptime is not None:
                if SeriesID != self.SeriesInstanceUID:
                    time.sleep(int(self.obj.sleeptime))
                    self.SeriesInstanceUID = SeriesID
        except Exception as e:
            logger.error("delayed:{}".format(e))
    # 停止
    def durationStop(self):
        # 改变状态
        self.Flag = False
        # 删除 文件夹
        shutil.rmtree(self.full_fn_fake)
        self.obj.sendstatus =False
        self.obj.save()

    def setParm(self, parm):  # 外部修改内部信息函数
        self.Parm = parm

    def getParm(self):  # 外部获得内部信息函数
        return self.parm
