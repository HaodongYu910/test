# coding= utf - 8
import queue

from django.contrib.sites import requests
import subprocess as sp
from .anonymization import *
import os
import logging
import random
import math
import socket
import time
from django.conf import settings
import threading
from AutoDicom.models import duration, dicom

logger = logging.getLogger(__name__)  # 这里使用 __name__ 动态搜索定义的 logger 配置


def get_date():
    # get current date
    localtime = time.localtime(time.time())
    return time.strftime("%Y%m%d", localtime)


def get_time():
    # get current time
    localtime = time.localtime(time.time())
    return time.strftime("%H%M%S", localtime)


def get_rand_uid():
    # generate a random value
    rand_val = random.randint(1, math.pow(10, 16) - 1)
    return "%08d" % rand_val


class DurationSendNewThread(threading.Thread):
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

    def anonymizationAndPutQueue(self, src_folder, study_infos_duration):
        '''
        input：
        src_folder: folder need be anonymization (can be a list)
        study_infos: empty dictionary{}

        key variable：
        full_fn:源文件绝对路径
        full_fn_fake:匿名后文件绝对路径（不包含该文件）
        file_after_fake:匿名后文件绝对路径（含该文件夹）
        study_info_duration: dictionary include all study infos (old StudyUID as key)
        q: queue, input is a list
        '''
        q = queue.Queue() # initial q
        for i in src_folder:
            # loop read src_folder path
            file_names = os.listdir(i)
            file_names.sort()
            for fn in tqdm(file_names):
                full_fn = os.path.join(i, fn)
                if os.path.isdir(full_fn):
                    self.anonymizationAndPutQueue(full_fn, study_infos_duration)
                    continue
                else:
                    ds = pydicom.dcmread(full_fn, force=True)  # 读取该路径文件的dicom信息
                    try:
                        if ds.StudyInstanceUID:
                            # and ds.PatientID and ds.PatientName: # 如果该文件存在UID等信息
                            oldUID = ds.StudyInstanceUID
                            if ds.StudyInstanceUID not in study_infos_duration.keys():  # 如果UID没在dic里面
                                study_infos_duration[oldUID] = {"patientID": {}, "patientName": {}, "AccessionNumber": {}, "StudyDate": {}, "StudyTime": {}, "SeriesDate": {}, "SeriesTime": {}, "newUID": {}, "No": {}}  # 在dic里面创建这个UID分支
                            try:
                                # 判断pID是否有值
                                if study_infos_duration[oldUID]["patientID"]:  # pid has value
                                    ds.PatientID = study_infos_duration[oldUID]["patientID"]
                                elif not study_infos_duration[oldUID]["patientID"]:  # no value
                                    ds.PatientID = self.norm_string(
                                        '{0}{1}'.format(self.patientid, get_rand_uid()), 24)
                                    study_infos_duration[oldUID]["patientID"] = ds.PatientID

                                if study_infos_duration[oldUID]["patientName"]:  # PN有值
                                    ds.PatientName = study_infos_duration[oldUID]["patientName"]
                                elif not study_infos_duration[oldUID]["patientName"]:  # PN没有值
                                    ds.PatientName = self.norm_string(
                                        '{0}{1}'.format(self.patientname, get_rand_uid()), 24)
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
                                    study_infos_duration[oldUID]["StudyTime"] = ds.StudyTime

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
                                    study_infos_duration[oldUID]["newUID"] = ds.StudyInstanceUID

                                study_infos_duration[oldUID]["No"] = nextNumber(self.full_fn_fake)
                                file_after_fake = '{0}/{1}.dcm'.format(self.full_fn_fake, str(study_infos_duration[oldUID]["No"]))
                                ds.save_as(file_after_fake)
                                logging.info("anon finished, current study info:[{0}]".format(study_infos_duration[oldUID]))
                                # tmp = study_infos_duration[oldUID]
                            except Exception as e:
                                logging.info(
                                    'failed to : file[{0}], error[{1}]'.format(full_fn, e))
                                continue

                            try:
                                info = {
                                    "rand_uid": study_infos_duration[oldUID]["newUID"],
                                    "cur_date": ds.StudyDate,
                                    "cur_time": ds.StudyTime,
                                    "path": file_after_fake
                                }
                                q.put([info, int(study_infos_duration[oldUID]["No"])])
                                # q is a list
                                logging.info("put in to q success. current queue length:[{0}]".format(q.qsize()))
                            except Exception as e:
                                logging.error("[匿名后加入q失败]:{}".format(e))
                                continue

                    except Exception as e:
                        logger.error('errormsg: failed to read file [{0}], it is not a dicom file'.format(full_fn))
                        continue
        return q

    def sync_send_file(self, q):
        # 发送数据
        """
        input: q[info,No] (default is a list)
        """
        while not q.empty():
            testdata = q.get()
            testdata_dic = testdata[0]
            file_name = testdata_dic["path"]
            studyuid = testdata_dic["rand_uid"]
            logging.info("prepare sending data [{0}]:[{1}]".format(studyuid,file_name))
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
                logging.info("storescu commands: [{0}]".format(commands) )
                popen.communicate()
                endtime = time.time()

                self.connect_influx({'studyuid': studyuid,
                                     'time': str('%.2f' % (float(endtime - starttime))),
                                     'starttime': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(starttime)),
                                     'endtime': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(endtime))

                                     })
                os.remove(file_name)
                logging.info("sending complete, current q size: [{0}]".format(q.qsize))
            except Exception as e:
                logging.error('send_file error: {0}'.format(e))

    def connect_influx(self, data):
        try:
            influxdata = 'duration,durationid={0},studyuid="{1}",starttime="{2}",endtime="{3}",avgtime="{4}"'.format(
                self.obj.id, data["studyuid"], data["starttime"], data["endtime"], data["time"])
            requests.post('http://192.168.1.121:8086/write?db=auto_test', data=influxdata)
            logging.info("update db success")
        except Exception as e:
            logger.error("保存connect_influx数据错误{}".format(e))

    def run(self):
        """
        input:
        self

        key variable:
        self.obj (duration object in django model class , complete setting id)
        """
        self.obj.sendstatus = False
        self.obj.save()
        dicom_folder_id = str(self.obj.dicom)
        dfi = dicom_folder_id.split(',') # split variable by ","
        dicom_folder_path = []
        for i in dfi:
            # loop read dicom_folder_path
            tmp = dicom.objects.filter(fileid=i)
            for j in tmp:
                dicom_folder_path.append(j.route)
        q = self.anonymizationAndPutQueue(dicom_folder_path,{}) # start anon and put data in q
        threads = []

        try:
            for i in range(self.thread_num):
                # limit thread number as default number 4.
                t = threading.Thread(target=self.sync_send_file, args=(q,))
                # args需要输出的是一个元组，如果只有一个参数，后面加，表示元组，否则会报错
                t.start()
                threads.append(t)
            for t in threads:
                t.join()
                time.sleep(1)
        except Exception as e:
            logger.error("multithread init error：{0}".format(e))

    def norm_string(self, str, len_norm):
        str_dest = str
        while len(str_dest) > len_norm or str_dest[0] == '.':
            str_dest = str_dest[1:]
        return str_dest