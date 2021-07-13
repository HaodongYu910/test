# coding=utf-8
import copy
import os
import pydicom
import logging
import subprocess as sp
import shutil
import socket
import requests
import time
import queue
from django.conf import settings
import threading
from AutoDicom.models import duration_record, dicom, duration, dicom_group_detail
from ..common.dataSort import *
logger = logging.getLogger(__name__)  # 这里使用 __name__ 动态搜索定义的 logger 配置


class DurationThread(threading.Thread):
    def __init__(self, **kwargs):
        threading.Thread.__init__(self)
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

    def anonymization(self, test_data):

        full_fn = test_data[0]
        full_fn_fake = test_data[1]
        info = test_data[2]
        saveID = test_data[3]
        try:
            ds = pydicom.dcmread(full_fn, force=True)
        except Exception as e:
            logging.error('errormsg: failed to read file [{0}]'.format(full_fn))
        try:
            studyolduid = ds.StudyInstanceUID
            Seriesinstanceuid = ds.SeriesInstanceUID
            acc_number = ds.AccessionNumber
            rand_uid = str(info.get("rand_uid"))
            fake_acc_number = self.norm_string("{0}_{1}".format(acc_number, rand_uid), 16)
            cur_date = get_date()
            cur_time = get_time()
        except Exception as e:
            logging.error(
                'failed to fake: file[{0}], error[{1}]'.format(full_fn, e))

        self.SeriesInstanceUID = ds.SeriesInstanceUID
        try:
            ds.SeriesInstanceUID = self.norm_string(
                '{0}.{1}'.format(ds.SeriesInstanceUID, rand_uid), 64)

            ds.SOPInstanceUID = self.norm_string(
                '{0}.{1}'.format(ds.SOPInstanceUID, rand_uid), 64)
            ds.StudyInstanceUID = info.get("study_uid")
            ds.PatientID = info.get("PatientID")
            ds.PatientName = info.get("PatientName")
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
        except Exception as e:
            logging.error(
                'failed to anonymous :  error[{}]'.format(e))

        try:
            ds.save_as(full_fn_fake)
        except Exception as e:
            logging.error('errormsg: failed to save file [{0}] --{1}'.format(full_fn_fake, e))

        try:
            if int(saveID) == 0:
                create_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
                data = {"patientid": info.get("PatientID"),
                        "patientname": info.get("PatientName"),
                        "accessionnumber": ds.AccessionNumber,
                        "studyinstanceuid": ds.StudyInstanceUID,
                        "studyolduid": studyolduid,
                        "sendserver": self.server,
                        "diseases": info.get("diseases"),
                        "relation_id": self.obj.id,
                        "update_time": create_time,
                        "create_time": create_time}
                duration_record.objects.create(**data)
        except Exception as e:
            logger.error('[获取数据失败]： [{0}]'.format(e))
        return Seriesinstanceuid

    def QueData(self):
        q = queue.Queue()
        filecount = 1
        dcmcount = 0
        dicomID = []
        # 查询 所以 dicom ID  优先组数据
        for i in dicom_group_detail.objects.filter(group__id__in=self.obj.dicom.split(",")):
            dicomID.append(i.dicom_id)

        # 查询发送数据
        dicomObj = dicom.objects.filter(id__in=dicomID, status=True)
        if len(dicomObj):
            dicomList = list(dicomObj)

            # 变成{"病种"：（病人对象，病人对象），"病种"：（病人对象，病人对象，...}
            dictsum = {}
            for i in dicomList:
                grouping(dictsum, i)

            # 变成排好序的数据
            listsum = Myinster(dictsum)
            # print(listsum)

            # 补充数据
            listsum = copylist(listsum, int(self.obj.sendcount))
            logger.info("listsum:{}".format(listsum))

            # 优先查询组
            for j in listsum:
                dcm = 0
                src_folder = str(j.route)
                while src_folder[-1] == '/':
                    src_folder = src_folder[0:-1]
                if not os.path.exists(src_folder):
                    os.system(f"rclone copy oss://qa-test-data/{j.route} {j.route}")
                try:
                    rand_uid = str(time.time())
                    info = {
                        "diseases": j.diseases,
                        "rand_uid": rand_uid,
                        "study_uid": self.norm_string('{0}.{1}'.format(j.studyinstanceuid, rand_uid), 64),
                        "PatientID": self.norm_string('{0}{1}'.format(j.patientid, self.patientid), 24),
                        "PatientName": self.norm_string('{0}{1}{2}'.format(str(j.diseases), self.patientname, rand_uid),
                                                        24)
                    }
                    file_names = os.listdir(src_folder)
                    file_names.sort()
                    for fn in file_names:
                        full_fn = os.path.join(src_folder, fn)
                        full_fn_fake = os.path.join(self.full_fn_fake, '{0}{1}'.format(filecount, fn))
                        if (os.path.splitext(fn)[1] in '.dcm' == False):
                            continue
                        try:
                            q.put([full_fn, full_fn_fake, info, dcm])
                            dcm = dcm + 1
                            logger.info("队列==", q)
                        except Exception as e:
                            logging.error("[匿名错误]:{}".format(e))
                            continue
                except Exception as e:
                    logger.error("遍历文件：{}".format(e))
                    continue
            return q

    # 匿名数据队列
    def run(self):
        q = self.QueData()
        if q is None:
            logger.info("没有有效数据发送")
            return False
        else:
            self.obj.sendstatus = True
            self.obj.save()
        threads = []

        try:
            logger.info("duration threading start")
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
            test_data = q.get()
            # logger.info(testdata)
            full_fn_fake = test_data[1]
            try:
                Seriesinstanceuid = self.anonymization(test_data)
            except Exception as e:
                logger.error("匿名失败:{}".format(e))

            try:
                self.sync_send_file(full_fn_fake, test_data[2]["study_uid"], Seriesinstanceuid)
            except Exception as e:
                logging.error('errormsg: failed to sync_send [{0}]---报错：{1}'.format(q.get()[1], e))
                continue
            try:
                self.delayed(Seriesinstanceuid)
            except Exception as e:
                logger.error("delayed fail:{}".format(e))

    # 存储 每张发送信息
    def connect_influx(self, data):
        try:
            tamp = int(round(time.time() * 1000000000))
            influxdata = f'test,id={self.obj.id},studyuid={data["studyuid"]},Seriesinstanceuid={data["Seriesinstanceuid"]} value={data["time"]} {tamp}'
            # logger.info(f"influx data:{influxdata}")
            requests.post('http://192.168.1.121:8086/write?db=auto_test', data=influxdata)
        except Exception as e:
            logger.error("保存connect_influx数据错误{}".format(e))

    def get_fake_name(self, rand_uid, fake_prefix):
        ts = time.localtime(time.time())
        return "{0}{1}{2}".format(fake_prefix, time.strftime("%m%d", ts), self.norm_string(rand_uid, 6))

    def sync_send_file(self, file_name, studyuid, Seriesinstanceuid):
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
                                 'starttime': starttime,
                                 'endtime': endtime,
                                 'Seriesinstanceuid':Seriesinstanceuid
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
        # 删除 文件夹
        shutil.rmtree(self.full_fn_fake)
        self.obj.sendstatus = False
        self.obj.save()
