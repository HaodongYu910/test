# coding=utf-8
import os
import shutil
import pydicom
import subprocess as sp
import datetime
import time
import queue
import threading

from AutoDicom.common.dataSort import *
from AutoDicom.models import duration_record, dicom
from AutoDicom.common.deletepatients import delete_patients_duration

from AutoProject.utils.graphql.graphql import *

from ..common.saveResult import ResultStatistics
from ..common.jmeter import JmeterThread
from ..models import stress, stress_record

from django.conf import settings
logger = logging.getLogger(__name__)  # 这里使用 __name__ 动态搜索定义的 logger 配置


class HybridThread(threading.Thread):
    def __init__(self, **kwargs):
        threading.Thread.__init__(self)
        self.Flag = True  # 停止标志位
        self.count = 0  # 可用来被外部访问
        self.obj = stress.objects.get(stressid=kwargs["stressid"])
        self.keyword = 'ST' + str(kwargs["stressid"])
        self.server = self.obj.Host.host
        self.thread_num = 4
        self.CountData = []
        self.local_aet = settings.LocalAet
        self.full_fn_fake = '{0}/{1}'.format(settings.LOG_PATH, self.keyword)

    # 匿名化数据
    def anonymization(self, test_data):

        full_fn = test_data[0]
        full_fn_fake = test_data[1]
        info = test_data[2]
        saveID = test_data[3]
        predictor = test_data[2].get("predictor")
        try:
            ds = pydicom.dcmread(full_fn, force=True)
        except Exception as e:
            logging.error('errormsg: failed to read file [{0}]'.format(full_fn))
        try:
            acc_number = ds.AccessionNumber
            rand_uid = str(info.get("rand_uid"))
            fake_acc_number = self.norm_string("{0}_{1}".format(acc_number, rand_uid), 16)
            cur_date = get_date()
            cur_time = get_time()
        except Exception as e:
            logging.error(
                'failed to fake: file[{0}], error[{1}]'.format(full_fn, e))

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

        except Exception as e:
            logging.error(
                'failed to anonymous :  error[{}]'.format(e))
        try:
            ds.save_as(full_fn_fake)
        except Exception as e:
            logging.error('errormsg: failed to save file [{0}] --{1}'.format(full_fn_fake, e))

        try:
            if int(saveID) == 0:
                stress_record.objects.create(**{
                    "version": self.obj.version,
                    "studyuid": ds.StudyInstanceUID,
                    "slicenumber": info.get("slicenumber"),
                    "images": info.get("images"),
                    "modelname": predictor,
                    "type": 'HH',
                    "Stress_id": self.obj.stressid,
                    "Host_id": self.obj.Host_id
                })
        except Exception as e:
            logger.error(f"stress_record.objects.create fail:{e}")
        try:
            self.sync_send_file(test_data[1], test_data[2]["study_uid"])
        except Exception as e:
            logging.error('errormsg: failed to sync_send [{0}]---报错：{1}'.format(test_data[1], e))

    # 混合测试列队
    def QueData(self):
        q = queue.Queue()
        filecount = 1
        dcmcount = 0
        logger.info("测试queue集合{}".format(self.obj.testdata.split(",")))
        # 查询发送数据
        dicomobj = dicom.objects.filter(predictor__in=self.obj.testdata.split(","),
                                        stressstatus__in=['1', '2'],
                                        status=True)

        if len(dicomobj):
            dicomList = list(dicomobj)
            # 变成{"病种"：（病人对象，病人对象），"病种"：（病人对象，病人对象，...}
            dictsum = {}
            for i in dicomList:
                grouping(dictsum, i)

            # 变成排好序的数据
            listsum = Myinster(dictsum)
            # print(listsum)

            # 补充数据
            listsum = copylist(listsum, int(self.obj.duration) * 50)

            # 优先查询组
            for j in listsum:
                dcmcount = 0
                src_folder = str(j.route)
                while src_folder[-1] == '/':
                    src_folder = src_folder[0:-1]
                try:
                    rand_uid = get_rand_uid()
                    info = {
                        "slicenumber": j.slicenumber,
                        "images": j.imagecount,
                        "predictor": j.predictor,
                        "rand_uid": rand_uid,
                        "study_uid": self.norm_string('{0}.{1}'.format(j.studyinstanceuid, rand_uid), 64),
                        "PatientID": self.norm_string('{0}st'.format(j.patientid), 24),
                        "PatientName": self.norm_string('{0}ST'.format(str(j.diseases)), 24)
                    }

                    file_names = os.listdir(src_folder)
                    file_names.sort()
                    for fn in file_names:
                        full_fn = os.path.join(src_folder, fn)
                        full_fn_fake = os.path.join(self.full_fn_fake, '{0}{1}'.format(filecount, fn))
                        if (os.path.splitext(fn)[1] in '.dcm' == False):
                            continue
                        try:
                            q.put([full_fn, full_fn_fake, info, dcmcount])
                            dcmcount = dcmcount + 1

                        except Exception as e:
                            logging.error("[匿名错误]:{}".format(e))
                            continue
                except Exception as e:
                    logger.error("遍历文件：{}".format(e))
            return q

    # 匿名混合测试
    def run(self):
        if not os.path.exists(self.full_fn_fake):
            os.makedirs(self.full_fn_fake)
        # 开始时间
        self.obj.start_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # 结束时间
        self.obj.end_date = (datetime.datetime.now() + datetime.timedelta(hours=int(self.obj.duration))).strftime(
            "%Y-%m-%d %H:%M:%S")
        self.obj.status = True
        self.obj.teststatus = '混合测试中'
        self.obj.save()
        if self.obj.jmeterstatus is True:
            jmeter = JmeterThread(stressid=self.obj.stressid)
            jmeter.setDaemon(True)
            jmeter.start()
        q = self.QueData()
        threads = []
        logger.info('-----------------------------混合测试开始-----------------------------')

        try:
            for i in range(self.thread_num):
                t = threading.Thread(target=self.durationAnony, args=(q,))
                # args需要输出的是一个元组，如果只有一个参数，后面加，表示元组，否则会报错
                t.start()
                threads.append(t)
            for t in threads:
                t.join()
                time.sleep(1)

            self.obj.status = False
            self.obj.teststatus = '测试结束'
            self.obj.save()

            Result = ResultStatistics(
                stressid=self.obj.stressid,
                stressType='HH'
            )
            Result.QueryResults()

        except Exception as e:
            logger.error("Thread Run Fail：{0}".format(e))

    # 混合测试发送数据
    def durationAnony(self, q):
        while not q.empty():
            # 开始时间
            start = datetime.datetime.now()
            if not os.path.exists(self.full_fn_fake) or str(start) > self.obj.end_date:
                break
            try:
                test_data = q.get()
                self.anonymization(test_data)
            except Exception as e:
                logger.error("匿名失败:{}".format(e))


    def sync_send_file(self, file_name, studyuid):
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

        drobj = duration_record.objects.filter(Duration="0{}".format(self.obj.stressid), imagecount=None)
        # 删除错误数据
        for j in drobj:
            delete_patients_duration(j.studyinstanceuid, self.obj.Host.id, "studyinstanceuid", False)
        drobj.delete()
        # 删除 文件夹
        folder = "/home/biomind/Biomind_Test_Platform/logs/ST{0}".format(str(self.id))
        if os.path.exists(folder):
            shutil.rmtree(folder)

    def setFlag(self, parm):  # 外部停止线程的操作函数
        if self.obj.jmeterstatus is True:
            stoptest = JmeterThread(stressid=self.obj.stressid)
            # 设为保护线程，主进程结束会关闭线程
            stoptest.setFlag = False
        # 删除 文件夹
        shutil.rmtree(self.full_fn_fake)
        self.Flag = parm  # boolean

    def setParm(self, parm):  # 外部修改内部信息函数
        self.Parm = parm

    def getParm(self):  # 外部获得内部信息函数
        return self.parm
