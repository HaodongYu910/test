# coding=utf-8
import logging
import threading
import os, shutil
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

from ..models import stress
from ..serializers import stress_result_Deserializer
from AutoDicom.models import duration_record, dicom
from AutoDicom.common.deletepatients import delete_patients_duration
from AutoDicom.serializers import duration_record_Serializer
from AutoDicom.common.dicomBase import checkuid, voteData

from AutoTest.utils.graphql.graphql import *
from AutoTest.utils.keycloak.login_kc import login_keycloak
from AutoTest.common.transport import SSHConnection
from AutoTest.models import Server, dictionary, uploadfile
from AutoTest.common.PostgreSQL import connect_postgres
from AutoTest.common.message import sendMessage

logger = logging.getLogger(__name__)  # 这里使用 __name__ 动态搜索定义的 logger 配置


# 删除dicom报告
def delreport(kc, studyinstanceuid):
    try:
        graphql_query = 'mutation{ ' \
                        'deleteReport( studyuid:' + str(studyinstanceuid) + ' )' \
                                                                            'deleteProtocol( studyuid:' + str(
            studyinstanceuid) + ' ) }'
        graphql_Interface(graphql_query, kc)
    except:
        logger.error("删除失败{0}".format(studyinstanceuid))


def get_date():
    localtime = time.localtime(time.time())
    return (time.strftime("%Y%m%d", localtime))


def get_time():
    localtime = time.localtime(time.time())
    return (time.strftime("%H%M%S", localtime))


def get_rand_uid():
    rand_val = random.randint(1, math.pow(10, 16) - 1)
    return "%08d" % rand_val


# 保存数据
def saveData(**kwargs):
    try:
        if kwargs["type"] in ["predictionJZ", "lung_prediction"]:
            sql = dictionary.objects.get(key="predictionJZ", type="sql", status=True)
            result = connect_postgres(database="orthanc", host=kwargs["id"],
                                      sql=sql.value.format(kwargs["studyuid"], kwargs["startdate"]))
            kwargs["datatest"]["type"] = kwargs["type"]
            try:
                kwargs["datatest"]["avg"] = str(result.to_dict(orient='records')[0]["avg"])
            except:
                kwargs["datatest"]["avg"] = 0
            try:
                kwargs["datatest"]["median"] = str(result.to_dict(orient='records')[0]["median"])
            except:
                kwargs["datatest"]["avg"] = 0
            try:
                kwargs["datatest"]["min"] = str(result.to_dict(orient='records')[0]["min"])
            except:
                kwargs["datatest"]["avg"] = 0
            try:
                kwargs["datatest"]["max"] = str(result.to_dict(orient='records')[0]["max"])
            except:
                kwargs["datatest"]["avg"] = 0
        else:
            kwargs["datatest"]["type"] = kwargs["type"]

        _result = stress_result_Deserializer(data=kwargs["datatest"])
        with transaction.atomic():
            _result.is_valid()
            _result.save()
    except Exception as e:
        logger.error("保存预测基准测试数据失败：{0}".format(e))


class STThread(threading.Thread):
    def __init__(self, **kwargs):
        threading.Thread.__init__(self)
        self.Flag = True  # 停止标志位
        self.count = 0  # 可用来被外部访问
        self.obj = stress.objects.get(stressid=kwargs["id"])
        self.keyword = 'ST' + str(kwargs["id"])
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

    #  基准测试
    def Manual(self):
        self.obj.status = True
        self.obj.save()
        count = int(self.obj.ramp)
        try:
            for i in self.obj.testdata.split(","):
                stressdata = dicom.objects.filter(predictor=i.strip(), stressstatus=2)
                for k in stressdata:
                    avglist = []
                    checkuid(self.obj.Host_id, self.server, str(k.id))
                    delreport(self.kc, str(k.studyinstanceuid))
                    # 循环 测试基准数据
                    startdate = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                    for j in range(count):
                        try:
                            if self.Flag is False:
                                break
                            # 开始时间
                            starttime = time.time()
                            result = graphql_Interface(k.graphql, self.kc)
                            ai_biomind = result['ai_biomind']
                            avgtime = time.time() - starttime
                            avglist.append(avgtime)
                            time.sleep(10)
                        except Exception as e:
                            logger.error("执行预测失败：{0}".format(k.studyinstanceuid))
                            continue

                    jobtype = 'jobJZ'
                    predictiontype = 'predictionJZ'
                    avgtime = str('%.2f' % np.mean(avglist))

                    datatest = {
                        "Stress": self.stressid,
                        "version": self.obj.version,
                        "count": count,
                        "modelname": k.predictor,
                        "slicenumber": k.slicenumber,
                        "avg": avgtime,
                        "min": str('%.2f' % min(avglist)),
                        "max": str('%.2f' % max(avglist)),
                        "minimages": k.imagecount,
                        "maximages": k.imagecount,
                        "avgimages": k.imagecount
                    }
                    saveData(datatest=datatest,
                             type=jobtype
                             )
                    saveData(datatest=datatest,
                             type=predictiontype,
                             id=self.obj.Host_id,
                             studyuid=k.studyinstanceuid,
                             startdate=startdate
                             )
            self.obj.status = False
            self.obj.save()
            sendMessage(touser='', toparty='132', message="【基准测试消息】\n 服务器：{0} 基准测试完成！~ 详细请查看！~ \n".format(self.obj.Host.host))
        except Exception as e:
            logger.error("执行预测基准测试数据失败：{0}".format(e))

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
            "duration_id": '0{}'.format(self.obj.stressid)
        }


    def QueData(self):
        q = queue.Queue()
        filecount = 1
        dcmcount = 0

        dicomobj = dicom.objects.filter(predictor__in=self.obj.testdata.split(","),
                                        stressstatus__in=['1', '2'],
                                        status=True)
        try:
            file_end = int(self.obj.loop_count)
            while True:
                if filecount > file_end:
                    self.CountData.append(dcmcount)
                    break
                if file_end >= filecount > int(dicomobj.count()):
                    dicomobj = dicom.objects.filter(predictor__in=self.obj.testdata.split(","),
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
                                full_fn_fake = os.path.join(self.full_fn_fake, '{0}{1}'.format(fn, filecount))
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

        except Exception as e:
            logger.error("队列生成失败：{0}".format(e))


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

            # try:
            #     study_fakeinfos["count"] = int(study_fakeinfos["count"]) + 1
            #     self.delayed(study_fakeinfos)
            # except Exception as e:
            #     logging.error('errormsg: failed delayed{0} ---报错：{1}]'.format(full_fn_fake, e))
            #     continue


    def connect_influx(self, data):
        try:
            influxdata = 'duration,durationid={0},studyuid="{1}",starttime="{2}",endtime="{3}",avgtime="{4}"'.format(
                self.obj.stressid, data["studyuid"], data["starttime"], data["endtime"], data["time"])
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
                self.obj.Host.host,
                self.obj.Host.port,
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
        self.Flag = parm  # boolean


    def setParm(self, parm):  # 外部修改内部信息函数
        self.Parm = parm


    def getParm(self):  # 外部获得内部信息函数
        return self.parm
