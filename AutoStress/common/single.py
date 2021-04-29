# coding=utf-8
import logging
import threading
import os
import shutil
import pydicom
import logging
import subprocess as sp
import time, datetime
import numpy as np
import random
import math
import socket
import requests
import time
import queue
from django.db import transaction
from django.conf import settings
import threading

from ..models import stress, stress_record
from ..serializers import stress_result_Deserializer
from AutoDicom.models import duration_record, dicom
from AutoDicom.common.deletepatients import delete_patients_duration

from AutoProject.utils.graphql.graphql import *
from AutoProject.common.transport import SSHConnection

from ..common.saveResult import ResultThread
from ..common.jmeter import JmeterThread

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


class SingleThread(threading.Thread):
    def __init__(self, **kwargs):
        threading.Thread.__init__(self)
        self.Flag = True  # 停止标志位
        self.count = 0  # 可用来被外部访问
        self.obj = stress.objects.get(stressid=kwargs["stressid"])
        self.keyword = 'SIN' + str(kwargs["stressid"])
        self.server = self.obj.Host.host
        self.thread_num = 4
        self.CountData = []

        # 获取计算机名称
        if socket.gethostname() == "biomindqa38":
            self.local_aet = 'QA38'
        else:
            self.local_aet = 'QA120'
        self.full_fn_fake = '{0}/{1}'.format(settings.LOG_PATH, self.keyword)
        if not os.path.exists(self.full_fn_fake):
            os.makedirs(self.full_fn_fake)

    # 匿名化数据
    def anonymization(self, full_fn, full_fn_fake, info):
        study_uid = ''
        series_uid = ''
        try:
            ds = pydicom.dcmread(full_fn, force=True)
        except Exception as e:
            logging.error('errormsg: failed to read file [{0}]'.format(full_fn))
        try:
            study_uid = ds.StudyInstanceUID
            acc_number = ds.AccessionNumber
            rand_uid = str(info.get("rand_uid"))
            fake_acc_number = self.norm_string("{0}_{1}".format(acc_number, rand_uid), 16)
            cur_date = info.get("cur_date")
            cur_time = info.get("cur_time")
            predictor = info.get("predictor")
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
            '{0}{1}{2}'.format(str(predictor), 'SIN', rand_uid), 24)

        ds.PatientName = self.norm_string(
            '{0}{1}{2}'.format(str(predictor), 'sin', rand_uid), 24)
        ds.AccessionNumber = fake_acc_number

        ds.StudyDate = cur_date
        ds.StudyTime = cur_time
        ds.SeriesDate = cur_date
        ds.SeriesTime = cur_time

        try:
            ds.save_as(full_fn_fake)
        except Exception as e:
            logging.error('errormsg: failed to save file [{0}] --{1}'.format(full_fn_fake, e))
        return {
            "version": self.obj.version,
            "studyuid": ds.StudyInstanceUID,
            "type": 'DY',
            "slicenumber":  info.get("slicenumber"),
            "images":  info.get("images"),
            "modelname": predictor,
            "Stress_id": self.obj.stressid,
            "Host_id": self.obj.Host_id
        }

    # 混合测试列队
    def QueData(self, model):
        q = queue.Queue()
        filecount = 1
        dcmcount = 0
        logger.info("测试模型：{}".format(model))
        dicomobj = dicom.objects.filter(predictor=model,
                                        stressstatus__in=['1', '2'],
                                        status=True)
        try:
            file_end = int(self.obj.loop_count)
            while True:
                if filecount > file_end:
                    self.CountData.append(dcmcount)
                    break
                if file_end >= filecount > int(dicomobj.count()):
                    logger.info("重新加载数据 file_end：{0}，{1}，{2}".format(file_end, filecount, int(dicomobj.count())))
                    dicomobj = dicom.objects.filter(predictor=model,
                                                    stressstatus__in=['1', '2'],
                                                    status=True)
                for j in dicomobj:
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
                                "slicenumber": j.slicenumber,
                                "images": j.imagecount,
                                "predictor": j.predictor,
                                "rand_uid": get_rand_uid(),
                                "cur_date": get_date(),
                                "cur_time": get_time()
                            }
                            file_names = os.listdir(src_folder)
                            file_names.sort()
                            for fn in file_names:
                                dcmcount = dcmcount + 1
                                full_fn = os.path.join(src_folder, fn)
                                full_fn_fake = os.path.join(self.full_fn_fake, '{0}{1}'.format(fn, filecount))
                                if (os.path.splitext(fn)[1] in ['.dcm'] == False):
                                    continue
                                try:
                                    # logger.info("队列数据:{}".format([full_fn, full_fn_fake, info, dcmcount]))
                                    q.put([full_fn, full_fn_fake, info, dcmcount])
                                except Exception as e:
                                    logging.error("[匿名错误]:{}".format(e))
                                    continue
                        except Exception as e:
                            logger.error("遍历文件：{}".format(e))
                    filecount = filecount + 1

            return q
        except Exception as e:
            logger.error("队列错误：{}".format(e))

    # 匿名混合测试
    def run(self):
        # 开始时间
        self.obj.teststatus = "单一开始"
        self.obj.status = True
        self.obj.save()

        # 按模型 循环预测
        for i in self.obj.testdata.split(","):
            try:
                q = self.QueData(model=i)
                threads = []
                self.obj.start_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                try:
                    for i in range(self.thread_num):
                        t = threading.Thread(target=self.durationAnony, args=(q,))
                        # args需要输出的是一个元组，如果只有一个参数，后面加，表示元组，否则会报错
                        t.start()
                        threads.append(t)
                    for t in threads:
                        t.join()
                        time.sleep(1)

                    self.obj.end_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    self.obj.save()

                    result = ResultThread(stressid=self.obj.stressid, stressType='DY')
                    result.setDaemon(True)
                    result.start()
                    time.sleep(180)
                    ssh = SSHConnection(host=self.obj.server, pwd=self.obj.Host.pwd)
                    ssh.command("nohup sshpass -p {} biomind restart > restart.log 2>&1 &".format(self.obj.Host.pwd))
                    time.sleep(500)
                except Exception as e:
                    logger.error("Thread Run Fail：{0}".format(e))
            except Exception as e:
                logger.error("Fail：{0}".format(e))

        self.obj.status = False
        self.obj.teststatus = '测试结束'
        self.obj.save()

    # 混合测试发送数据
    def durationAnony(self, q):
        while not q.empty():
            if self.Flag is False:
                break
            testdata = q.get()
            full_fn_fake = testdata[1]
            try:
                data = self.anonymization(testdata[0], full_fn_fake, testdata[2])
            except Exception as e:
                logger.error("匿名失败:{}".format(e))
            try:
                if testdata[3] in self.CountData:
                    stress_record.objects.create(**data)
            except Exception as e:
                logger.error('[获取数据失败]： [{0}]'.format(e))
            try:
                self.sync_send_file(full_fn_fake)
            except Exception as e:
                logging.error('errormsg: failed to sync_send [{0}]---报错：{1}'.format(q.get()[1], e))
                continue


    def get_fake_name(self, rand_uid, fake_prefix):
        ts = time.localtime(time.time())
        return "{0}{1}{2}".format(fake_prefix, time.strftime("%m%d", ts), self.norm_string(rand_uid, 6))

    def sync_send_file(self, file_name):
        # 发送数据
        try:
            commands = [
                "storescu",
                self.obj.Host.host,
                self.obj.Host.port,
                "-aec", self.obj.Host.remarks,
                "-aet", self.local_aet,
                file_name
            ]
            popen = sp.Popen(commands, stderr=sp.PIPE, stdout=sp.PIPE, shell=False)
            popen.communicate()
            os.remove(file_name)
        except Exception as e:
            logging.error('send_file error: {0}'.format(e))

    def norm_string(self, str, len_norm):
        str_dest = str
        while len(str_dest) > len_norm or str_dest[0] == '.':
            str_dest = str_dest[1:]
        return str_dest

    def durationStop(self):
        # 改变状态
        self.obj.status = False
        self.obj.save()
        self.Flag = False
        # 删除 文件夹
        folder = "/home/biomind/Biomind_Test_Platform/logs/ST{0}".format(str(self.id))
        if os.path.exists(folder):
            shutil.rmtree(folder)


    def setFlag(self, parm):  # 外部停止线程的操作函数
        if self.obj.jmeterstatus is True:
            stoptest = JmeterThread(stressid=self.obj.stressid)
            # 设为保护线程，主进程结束会关闭线程
            stoptest.setFlag = False
        self.Flag = parm  # boolean

    def setParm(self, parm):  # 外部修改内部信息函数
        self.Parm = parm

    def getParm(self):  # 外部获得内部信息函数
        return self.parm
