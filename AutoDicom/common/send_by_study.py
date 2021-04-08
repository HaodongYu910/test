# coding= utf - 8
import queue

from django.contrib.sites import requests
from pandas.tests.sparse.frame.test_to_from_scipy import scipy as sp

from .anonymization import *
import os
import pydicom
import logging
import random
import math
import socket
import time
from django.conf import settings
import threading
from AutoDicom.models import duration

logger = logging.getLogger(__name__)  # 这里使用 __name__ 动态搜索定义的 logger 配置


def get_date():
    localtime = time.localtime(time.time())
    return time.strftime("%Y%m%d", localtime)


def get_time():
    localtime = time.localtime(time.time())
    return time.strftime("%H%M%S", localtime)


def get_rand_uid():
    rand_val = random.randint(1, math.pow(10, 16) - 1)
    return "%08d" % rand_val


class DurationThread(threading.Thread):
    def __init__(self, **kwargs):
        threading.Thread.__init__(self)
        self.Flag = True  # 停止标志位
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

    def anonymizationAndPutQueue(self, src_folder, study_infos_duration, anonkey):
        '''
        src_folder: folder need be anonymization
        study_infos: empty dictionary{}
        diseases: input parameter from front
        wPN:boolean值，是否匿名patient name
        wPID:boolean值，是否匿名patient ID
        anonkey:匿名化key值
        '''
        q = queue.Queue()
        file_names = os.listdir(src_folder)
        file_names.sort()
        for fn in tqdm(file_names):
            full_fn = os.path.join(src_folder, fn)
            if os.path.isdir(full_fn):
                self.anonymizationAndPutQueue(self, full_fn, study_infos_duration, anonkey)
                logging.info('-------------this is a folder,skiping....')
                continue
            else:
                ds = pydicom.dcmread(full_fn, force=True)  # 读取该路径文件的dicom信息
                try:
                    if ds.StudyInstanceUID:
                        # and ds.PatientID and ds.PatientName: # 如果该文件存在UID等信息
                        logging.info('1. this is a truly dicom document')
                        if ds.StudyInstanceUID not in study_infos_duration.keys():  # 如果UID没在dic里面
                            study_infos_duration[oldUID] = {"patientID": {}, "patientName": {}}  # 在dic里面创建这个UID分支
                            oldUID = ds.StudyInstanceUID
                            logging.info('2. insert UID in dic')
                        try:

                            # 判断pID是否有值
                            if study_infos_duration[oldUID]["patientID"]:  # pid has value
                                ds.PatientID = study_infos_duration[oldUID]["patientID"]
                            elif not study_infos_duration[oldUID]["patientID"]:  # no value
                                ds.PatientID = norm_string(
                                    "{0}_{1}{2}".format(anonkey, time.strftime("%H%M%S", time.localtime(time.time())),
                                                        randomFourNum(4)), 32)
                                study_infos_duration[oldUID]["patientID"] = ds.PatientID

                            if study_infos_duration[oldUID]["patientName"]:  # PN有值
                                ds.PatientName = study_infos_duration[oldUID]["patientName"]
                            elif not study_infos_duration[oldUID]["patientName"]:  # PN没有值
                                ds.PatientName = norm_string(
                                    "{0}_{1}{2}".format(anonkey, time.strftime("%H%M%S", time.localtime(time.time())),
                                                        randomFourNum(4)), 32)
                                study_infos_duration[oldUID]["patientName"] = ds.PatientName

                            # if study_infos_duration[oldUID]["SOPInstanceUID"]:  # SOPInstanceUID有值
                            #     ds.SOPInstanceUID = study_infos_duration[oldUID]["SOPInstanceUID"]
                            # elif not study_infos_duration[oldUID]["SOPInstanceUID"]:  # 没有值
                            #     ds.SOPInstanceUID = norm_string(
                            #         '{0}.{1}'.format(ds.SOPInstanceUID, get_rand_uid()), 64)
                            #     study_infos_duration[oldUID]["SOPInstanceUID"] = ds.SOPInstanceUID

                            if study_infos_duration[oldUID]["AccessionNumber"]:  # AccessionNumber有值
                                ds.AccessionNumber = study_infos_duration[oldUID]["AccessionNumber"]
                            elif not study_infos_duration[oldUID]["AccessionNumber"]:  # 没有值
                                ds.AccessionNumber = norm_string("{0}_{1}".format(ds.AccessionNumber, get_rand_uid()),
                                                                 16)
                                study_infos_duration[oldUID]["AccessionNumber"] = ds.AccessionNumber

                            if study_infos_duration[oldUID]["StudyDate"]:  # StudyDate有值
                                ds.StudyDate = study_infos_duration[oldUID]["StudyDate"]
                            elif not study_infos_duration[oldUID]["patientName"]:  # 没有值
                                ds.StudyDate = get_date()
                                study_infos_duration[oldUID]["StudyDate"] = ds.StudyDate

                            if study_infos_duration[oldUID]["StudyTime"]:  # StudyTime有值
                                ds.StudyTime = study_infos_duration[oldUID]["StudyTime"]
                            elif not study_infos_duration[oldUID]["StudyTime"]:  # 没有值
                                ds.StudyTime = get_time()
                                study_infos_duration[oldUID]["StudyDate"] = ds.StudyTime

                            if study_infos_duration[oldUID]["SeriesDate"]:  # SeriesDate有值
                                ds.SeriesDate = study_infos_duration[oldUID]["SeriesDate"]
                            elif not study_infos_duration[oldUID]["SeriesDate"]:  # 没有值
                                ds.SeriesDate = get_date()
                                study_infos_duration[oldUID]["SeriesDate"] = ds.SeriesDate

                            if study_infos_duration[oldUID]["SeriesTime"]:  # SeriesTime有值
                                ds.SeriesTime = study_infos_duration[oldUID]["SeriesTime"]
                            elif not study_infos_duration[oldUID]["SeriesTime"]:  # 没有值
                                ds.SeriesTime = get_time()
                                study_infos_duration[oldUID]["SeriesTime"] = ds.SeriesTime

                            if study_infos_duration[oldUID]["newUID"]:  # suid有值
                                ds.StudyInstanceUID = study_infos_duration[oldUID]["newUID"]
                            elif not study_infos_duration[oldUID]["newUID"]:  # 没有值
                                ds.StudyInstanceUID = norm_string(
                                    '{0}.{1}'.format(ds.StudyInstanceUID, get_rand_uid()), 64)
                                study_infos_duration[oldUID]["suid"] = ds.StudyInstanceUID

                            study_infos_duration[oldUID]["No"] = nextNumber(self.full_fn_fake)
                            file_after_fake = '{0}/{1}.dcm'.format(self.full_fn_fake, str(study_infos_duration[oldUID]["No"]))
                            ds.save_as(file_after_fake)
                            # tmp = study_infos_duration[oldUID]
                        except Exception as e:
                            logging.info(
                                'failed to : file[{0}], error[{1}]'.format(full_fn, e))
                            continue

                        try:
                            info = {
                                "rand_uid": study_infos_duration[oldUID]["newUID"],
                                "cur_date": ds.StudyDate,
                                "cur_time": ds.StudyTime()
                            }
                            q.put(full_fn,file_after_fake, info , study_infos_duration[oldUID]["No"])
                        except Exception as e:
                            logging.error("[匿名后加入q失败]:{}".format(e))
                            continue

                except Exception as e:
                    logger.error('errormsg: failed to read file [{0}], it is not a dicom file'.format(full_fn))
                    continue
        return q

    def sync_send_file(self, q):
        # 发送数据
        while not q.empty():
            testdata = q.get()
            file_name = testdata[1]
            studyuid = testdata[2]["rand_uid"]
        try:
            commands = [
                "storescu",
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

    def connect_influx(self, data):
        try:
            influxdata = 'duration,durationid={0},studyuid="{1}",starttime="{2}",endtime="{3}",avgtime="{4}"'.format(
                self.obj.id, data["studyuid"], data["starttime"], data["endtime"], data["time"])
            requests.post('http://192.168.1.121:8086/write?db=auto_test', data=influxdata)
        except Exception as e:
            logger.error("保存connect_influx数据错误{}".format(e))

    def run(self):
        self.obj.sendstatus = False
        self.obj.save()
        q = self.anonymizationAndPutQueue()
        threads = []

        try:
            for i in range(self.thread_num):
                t = threading.Thread(target=self.sync_send_file(q))
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

        except Exception as e:
            logger.error("队列生成失败：{0}".format(e))