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
import threading
import time
import queue

from AutoStress.models import stress, Server
from AutoTest.common.PostgreSQL import connect_postgres
from AutoTest.common.api_response import JsonResponse

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
        for i in self.obj.dicom.split(","):
            try:
                dicomobj = dicom.objects.filter(fileid=str(i), status=True)
            except Exception as e:
                continue
            for j in dicomobj:
                try:
                    delete_patients_duration(j.studyinstanceuid, self.obj.Host, 'StudyInstanceUID', False)
                except Exception as e:
                    logger.error("删除数据失败:{}".format(e))
                try:
                    self.sendDicom(j.route)
                except Exception as e:
                    logger.error("发送数据失败：{}".format(e))


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
        folder = "/home/biomind/Biomind_Test_Platform/logs/{0}{1}{2}".format(str(self.obj.patientname), str(self.obj.patientid),
                                                                             str(self.id))
        if os.path.exists(folder):
            shutil.rmtree(folder)

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



class SendThread(threading.Thread):
    def __init__(self, *args, **kwargs):
        threading.Thread.__init__(self)
        self.Flag = True  # 停止标志位
        # self.count = kwargs["count"]  # 可用来被外部访问的
        if kwargs["type"] == 'stress':
            obj = dicom.objects.filter(predictor=kwargs["predictor"])
        else:
            obj = dicom.objects.filter(id=kwargs["id"])

        self.Hostobj = Server.objects.get(id=kwargs["hostid"])
        self.server = self.Hostobj.host

        log_path = "/files/durationlog/{}".format(self.keyword)
        if not os.path.exists(log_path):
            os.makedirs(log_path)

        log_file = '{0}/sendinfo.log'.format(log_path)
        self.logging.basicConfig(filename=log_file, filemode='a+',
                                 format="%(asctime)s [%(funcName)s:%(lineno)s] %(levelname)s: %(message)s",
                                 datefmt="%Y-%m-%d %H:%M:%S", level=logging.DEBUG)

    # 检查是否数据
    def checkuid(self, dicomid):
        obj = dicom.objects.get(id=dicomid)
        sql = 'select studyinstanceuid,patientname from study_view where studyinstanceuid = \'{0}\''.format(
            obj.studyinstanceuid)
        result_db = connect_postgres(host=self.Hostobj.host, sql=sql)
        # 无此数据，发送
        if len(result_db) == 0:
            self.Send(obj.route)
        # 重复数据 先删除后再发送新数据
        elif len(result_db) > 2:
            delete_patients_duration(obj.studyinstanceuid, self.Hostobj.id, 'StudyInstanceUID', False)
            self.Send(obj.route)

    def connect_influx(self,data):
        posturl = 'http://192.168.1.121:8086/write?db=autotest'
        requests.post(posturl, data=data)

    def get_date(self):
        localtime = time.localtime(time.time())
        return (time.strftime("%Y%m%d", localtime))

    def get_time(self):
        localtime = time.localtime(time.time())
        return (time.strftime("%H%M%S", localtime))

    def get_rand_uid(self):
        rand_val = random.randint(1, math.pow(10, 16) - 1)
        return "%08d" % rand_val

    def get_fake_name(self,rand_uid, fake_prefix):
        ts = time.localtime(time.time())
        return "{0}{1}{2}".format(fake_prefix, time.strftime("%m%d", ts), self.norm_string(rand_uid, 6))

    def sync_send_file(self,file_name, commands):
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

    def norm_string(self,str, len_norm):
        str_dest = str
        while len(str_dest) > len_norm or str_dest[0] == '.':
            str_dest = str_dest[1:]
        return str_dest

    def get_fake_accession_number(self,acc_number, rand_uid):
        str = "{0}_{1}".format(acc_number, rand_uid)
        return self.norm_string(str, 16)

    def get_study_fakeinfo(self,studyuid, acc_number, study_fakeinfos):
        if not study_fakeinfos.get(studyuid):
            rand_uid = self.get_rand_uid()
            # "fake_name": get_fake_name(rand_uid, keyword),
            info = {
                "rand_uid": rand_uid,
                "fake_acc_num": self.get_fake_accession_number(acc_number, rand_uid),
                "cur_date": self.get_date(),
                "cur_time": self.get_time()
            }
            study_fakeinfos[studyuid] = info
        fake_info = study_fakeinfos[studyuid]
        logging.info("---debug{}".format(fake_info))
        return fake_info

    # 判断是否 同一个 Series
    def delayed(self,Seriesinstanceuid, image, CONFIG):
        if image["count"] == int(CONFIG.get('sleepcount', '')):
            time.sleep(int(CONFIG.get('sleeptime', '')))
            image["count"] = 0
        if CONFIG.get('Seriesinstanceuid', '') != Seriesinstanceuid and CONFIG.get('Series', '') == '1':
            time.sleep(int(CONFIG.get('sleeptime', '')))
            CONFIG["Seriesinstanceuid"] = Seriesinstanceuid

    # 匿名数据
    def anonymization(self, full_fn, full_fn_fake, diseases, CONFIG):
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
            study_fakeinfo = self.get_study_fakeinfo(study_uid, acc_number, self.study_fakeinfos)
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

        instance_uid = ''
        try:
            instance_uid = ds.SOPInstanceUID
        except Exception as e:
            logging.error(
                'failed to fake sopinstanceuid: file[{0}], error[{1}]'.format(full_fn, e))
        ds.SOPInstanceUID = self.norm_string(
            '{0}.{1}'.format(instance_uid, rand_uid), 64)
        ds.PatientID = self.norm_string(
            '{0}{1}{2}'.format(str(diseases), str(CONFIG["patientid"]), rand_uid), 24)

        ds.PatientName = self.norm_string(
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
    def fake_folder(self,folder, folder_fake, study_fakeinfos, study_infos, image, diseases, CONFIG):
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
                self.fake_folder(full_fn, full_fn_fake, study_fakeinfos, study_infos, image, diseases, CONFIG)
                continue
            try:
                newstudyuid, newpatientid, newpatientname, studyolduid, accessionNumber, Seriesinstanceuid = self.anonymization(
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
                start, end, diff = self.sync_send_file(full_fn_fake, commands)
            except Exception as e:
                logging.error('errormsg: failed to sync_send [{0}]'.format(full_fn_fake))
                continue
            try:
                sqldata = "INSERT INTO duration_record values(NULL,\'{0}\', \'{1}\', \'{2}\', \'{3}\', \'{4}\', NULL, NULL,NULL, NULL,\'{5}\',\'{6}\', \'{7}\', \'{8}\',\'{9}\', \'{10}\',\'{11}\')".format(
                    newpatientid, newpatientname, accessionNumber, newstudyuid, studyolduid, CONFIG['ip'], start,
                    start, diff, start, end, int(CONFIG.get('durationid', '')))

            except Exception as e:
                logging.error('errormsg: failed to save_send_record file [{0}][[1]]'.format(full_fn, e))
                continue
            try:
                image["count"] = int(image["count"]) + 1
                self.delayed(Seriesinstanceuid, image, CONFIG)
            except Exception as e:
                logging.error('errormsg: failed delayed{0}]'.format(full_fn_fake))
                continue

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