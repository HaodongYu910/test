# coding=utf-8
import logging
import threading
import os, shutil
import pydicom
import logging
import subprocess as sp
import datetime
import random
import math
import socket
import requests
import threading
import time
import queue

from AutoStress.models import stress, Server
from AutoProject.common.PostgreSQL import connect_postgres
from AutoProject.common.api_response import JsonResponse

from .deletepatients import delete_patients_duration
from ..models import duration_record, dicom, duration

logger = logging.getLogger(__name__)  # 这里使用 __name__ 动态搜索定义的 logger 配置


class DicomThread(threading.Thread):
    def __init__(self, *args, **kwargs):
        threading.Thread.__init__(self)
        self.Flag = True  # 停止标志位
        # self.count = kwargs["count"]  # 可用来被外部访问的
        #
        self.type = kwargs["type"]
        if kwargs["type"] == 'stress':
            self.obj = stress.objects.get(stressid=kwargs["stressid"])
            self.keyword = str(stress) + str(kwargs["stressid"])
            self.id = kwargs["stressid"]

        elif kwargs["type"] == 'duration':
            self.obj = duration.objects.get(id=kwargs["id"])
            self.keyword = str(self.obj.patientname) + str(self.obj.patientid) + str(kwargs["id"])
            self.id = kwargs["id"]
        else:
            self.stressid = kwargs["stressid"]
        self.server = self.obj.Host.host

    # 匿名发送
    def anonymousSend(self):
        a = 0
        nom = 0
        try:
            sleepcount = self.obj.sleepcount if self.obj.sleepcount is not None else 9999
            sleeptime = self.obj.sleeptime if self.obj.sleeptime is not None else 0
            patientid = self.obj.patientid if self.obj.patientid is not None else '_'
            patientname = self.obj.patientname if self.obj.patientname is not None else '_'
            if self.obj.series is True:
                series = 1
            else:
                series = 0

            if self.obj.sendcount is None and self.obj.end_time is None:
                end = 1
            elif self.obj.sendcount is None and self.obj.end_time is not None:
                end = (datetime.datetime.now() + datetime.timedelta(hours=int(self.obj.end_time))).strftime(
                    "%Y-%m-%d %H:%M:%S")
            else:
                for j in self.obj.dicom.split(","):
                    nom = nom + 1
                imod = divmod(int(self.obj.sendcount), nom)
                if imod[0] < 1:
                    return JsonResponse(code="999994", msg="少于病种数量，请增加发送数量！")
            for i in self.obj.dicom.split(","):
                if nom != 0:
                    end = int(imod[0]) + int(imod[1]) if a == 0 else int(imod[0])
                    a = a + 1
                cmd = ('nohup /home/biomind/.local/share/virtualenvs/biomind-dvb8lGiB/bin/python3'
                       ' /home/biomind/Biomind_Test_Platform/AutoDicom/common/dicomSend.py '
                       '--ip {0} --aet {1} '
                       '--port {2} '
                       '--patientid {3} '
                       '--patientname {4} '
                       '--folderid {5} '
                       '--durationid {6} '
                       '--end {7} '
                       '--sleepcount {8} '
                       '--sleeptime {9} '
                       '--series {10} &').format(self.obj.server, self.obj.aet, self.obj.port, patientid, patientname,
                                                 i, self.id,
                                                 end, sleepcount, sleeptime, series)
                logger.info(cmd)
                os.system(cmd)
                time.sleep(1)
            self.obj.sendstatus = True
            self.obj.save()
            return True

        except Exception as e:
            return False
            logger.error("发送失败：{0}".format(e))

    # 正常发送
    def normalSend(self):
        self.obj.sendstatus = True
        self.obj.save()
        try:
            dicomobj = dicom.objects.filter(fileid__in=self.obj.dicom.split(","), status=True)
        except Exception as e:
            logger.error(e)
        for j in dicomobj:
            try:
                delete_patients_duration(j.studyinstanceuid, self.obj.Host, 'StudyInstanceUID', False)
            except Exception as e:
                logger.error("删除数据失败:{}".format(e))
            try:
                self.sendDicom(j.route)
            except Exception as e:
                logger.error("发送数据失败：{}".format(e))

    def sendDicom(self, route):
        try:
            src_folder = route
            while src_folder[-1] == '/':
                src_folder = src_folder[0:-1]
            self.fake_folder(src_folder)
        except Exception as e:
            logging.error("error: failed to send", e)

    def sync_send_file(self, file_name):
        # 发送数据
        try:
            # 获取计算机名称
            if socket.gethostname() == "biomindqa38":
                local_aet = 'QA38'
            else:
                local_aet = 'QA120'

            # logging.info('send file: [{0}]'.format(file_name))
            commands = [
                "storescu",
                self.obj.Host.host,
                self.obj.Host.port,
                "-aec", self.obj.Host.remarks,
                "-aet", local_aet,
                file_name
            ]
            popen = sp.Popen(commands, stderr=sp.PIPE, stdout=sp.PIPE, shell=False)
            popen.communicate()
        except Exception as e:
            logging.error('send_file error: {0}'.format(e))

    def fake_folder(self, folder):
        file_names = os.listdir(folder)
        file_names.sort()

        for fn in file_names:
            full_fn = os.path.join(folder, fn)
            if (os.path.splitext(fn)[1] in ['.dcm'] == False):
                continue
            elif (os.path.isdir(full_fn)):
                self.fake_folder(full_fn)
                continue
            try:
                self.sync_send_file(full_fn)
            except Exception as e:
                logging.error('errormsg: failed to sync_send file [{0}][[1]]'.format(full_fn, e))
                continue

    def setFlag(self, parm):  # 外部停止线程的操作函数
        self.Flag = parm  # boolean

    def setParm(self, parm):  # 外部修改内部信息函数
        self.Parm = parm

    def getParm(self):  # 外部获得内部信息函数
        return self.parm

# 发送文件
class SendQueThread:
    def __init__(self, **kwargs):
        self.thread_num = 4
        self.route = kwargs["route"]
        self.hostobj = Server.objects.get(id=kwargs["hostid"])
        self.routelist = []

        # 获取计算机名称
        if socket.gethostname() == "biomindqa38":
            self.local_aet = 'QA38'
        else:
            self.local_aet = 'QA120'

    def run(self):
        try:
            src_folder = self.route
            while src_folder[-1] == '/':
                src_folder = src_folder[0:-1]
            self.fake_folder(src_folder)
        except Exception as e:
            logging.error("error: failed to send", e)
        # 添加队列
        q = queue.Queue()
        for i in self.routelist:
            commands = [
                "storescu",
                self.hostobj.host,
                self.hostobj.port,
                "-aec", self.hostobj.remarks,
                "-aet", self.local_aet,
                i
            ]
            q.put(commands)  # 往队列里生成消息

        threads = []
        for i in range(self.thread_num):
            t = threading.Thread(target=self.send, args=(q,))
            # args需要输出的是一个元组，如果只有一个参数，后面加，表示元组，否则会报错
            threads.append(t)
        for i in range(self.thread_num):
            threads[i].start()
        for i in range(self.thread_num):
            threads[i].join()

    # 下面来通过多线程来处理Queue里面的任务：
    def send(self, q):
        while True:
            if q.empty():
                return
            else:
                try:
                    commands = q.get()
                    starttime = time.time()
                    popen = sp.Popen(commands, stderr=sp.PIPE, stdout=sp.PIPE, shell=False)
                    popen.communicate()
                    endtime = time.time()
                    # diff = str('%.2f' % (float(endtime - starttime)))
                    # start = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(starttime))
                    # end = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(endtime))
                except Exception as e:
                    logging.error('send_file error: {0}'.format(e))

    def fake_folder(self, folder):
        file_names = os.listdir(folder)
        file_names.sort()

        for fn in file_names:
            full_fn = os.path.join(folder, fn)
            if (os.path.splitext(fn)[1] in ['.dcm'] == False):
                continue
            elif (os.path.isdir(full_fn)):
                self.fake_folder(full_fn)
                continue
            try:
                self.routelist.append(full_fn)
            except Exception as e:
                logging.error('errormsg: file [{0}][[1]]'.format(full_fn, e))
                continue

# if __name__ == "__main__":
#     start = time.time()
#     # main()
#     # print('耗时：', time.time() - start)
