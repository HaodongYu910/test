# coding=utf-8
import logging
from TestPlatform.models import GlobalHost,duration_record
import threading
import os, shutil
import pydicom
import logging
import subprocess as sp
import time, datetime
import random
import math
from TestPlatform.common.api_response import JsonResponse
import socket
from TestPlatform.models import dicom, duration
from Stress.models import stress
from .deletepatients import delete_patients_duration

logger = logging.getLogger(__name__)  # 这里使用 __name__ 动态搜索定义的 logger 配置


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
        self.Hostobj = GlobalHost.objects.get(id=self.obj.hostid)
        self.server = self.Hostobj.host

    # 匿名发送
    def anonymousSend(self):
        a = 0
        nom = 0
        try:
            sleepcount = self.obj.sleepcount if self.obj.sleepcount is not None else 9999
            sleeptime = self.obj.sleeptime if self.obj.sleeptime is not None else 0
            patientid = self.obj.patientid if self.obj.patientid is not None else '_'
            patientname = self.obj.patientname if self.obj.patientname is not None else '_'
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
                       ' /home/biomind/Biomind_Test_Platform/Dicom/common/dicomSend.py '
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
                                                 end, sleepcount, sleeptime, self.obj.series)
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
        for i in self.obj.dicom.split(","):
            try:
                dicomobj = dicom.objects.filter(fileid=str(i), status=True)
            except Exception as e:
                continue
            for j in dicomobj:
                delete_patients_duration(j.studyinstanceuid, self.obj.hostid, 'StudyInstanceUID', False)

            time.sleep(1)

        self.obj.sendstatus = True
        self.obj.save()

    def durationStop(self):
        # 改变状态
        self.obj.sendstatus = False
        self.obj.save()
        drobj = duration_record.objects.filter(duration_id=self.id, imagecount=None)
        # 删除错误数据
        for j in drobj:
            delete_patients_duration(j.studyinstanceuid, self.obj.hostid, "studyinstanceuid", False)
        drobj.delete()
        # 删除 文件夹
        folder = "/home/biomind/Biomind_Test_Platform/logs/{0}{1}{2}".format(str(self.obj.patientname), str(self.obj.patientid),
                                                                             str(self.id))
        if os.path.exists(folder):
            shutil.rmtree(folder)

    def setFlag(self, parm):  # 外部停止线程的操作函数
        self.Flag = parm  # boolean


    def setParm(self, parm):  # 外部修改内部信息函数
        self.Parm = parm


    def getParm(self):  # 外部获得内部信息函数
        return self.parm


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



class SendThread(threading.Thread):
    def __init__(self, *args, **kwargs):
        threading.Thread.__init__(self)
        self.Flag = True  # 停止标志位
        # self.count = kwargs["count"]  # 可用来被外部访问的
        if kwargs["type"] == 'stress':
            obj = dicom.objects.filter(predictor=kwargs["predictor"])
        else:
            obj = dicom.objects.filter(id=kwargs["id"])

        self.Hostobj = GlobalHost.objects.get(id=kwargs["hostid"])
        self.server = self.Hostobj.host

        log_path = "/files/durationlog/{}".format(self.keyword)
        if not os.path.exists(log_path):
            os.makedirs(log_path)

        log_file = '{0}/sendinfo.log'.format(log_path)
        self.logging.basicConfig(filename=log_file, filemode='a+',
                                 format="%(asctime)s [%(funcName)s:%(lineno)s] %(levelname)s: %(message)s",
                                 datefmt="%Y-%m-%d %H:%M:%S", level=logging.DEBUG)

    # def Send(self):
    #     try:
    #         src_folder = route
    #         while src_folder[-1] == '/':
    #             src_folder = src_folder[0:-1]
    #         fake_folder(serverID, src_folder)
    #     except Exception as e:
    #         logging.error("error: failed to send", e)

    # 正常发送
    def normalSend(self):
        for i in self.obj.dicom.split(","):
            try:
                dicomobj = dicom.objects.filter(fileid=str(i), status=True)
            except Exception as e:
                continue
            for j in dicomobj:
                delete_patients_duration(j.studyinstanceuid, self.obj.hostid, 'StudyInstanceUID', False)

            time.sleep(1)

        self.obj.sendstatus = True
        self.obj.save()

    def durationStop(self):
        # 改变状态
        self.obj.sendstatus = False
        self.obj.save()
        drobj = duration_record.objects.filter(duration_id=self.id, imagecount=None)
        # 删除错误数据
        for j in drobj:
            delete_patients_duration(j.studyinstanceuid, self.obj.hostid, "studyinstanceuid", False)
        drobj.delete()
        # 删除 文件夹
        folder = "/home/biomind/Biomind_Test_Platform/logs/{0}{1}{2}".format(str(self.obj.patientname), str(self.obj.patientid),
                                                                             str(self.id))
        if os.path.exists(folder):
            shutil.rmtree(folder)

    def setFlag(self, parm):  # 外部停止线程的操作函数
        self.Flag = parm  # boolean


    def setParm(self, parm):  # 外部修改内部信息函数
        self.Parm = parm


    def getParm(self):  # 外部获得内部信息函数
        return self.parm
