# coding=utf-8
import os
import shutil
import pydicom
import subprocess as sp
import datetime
import socket
import time
import queue
from django.conf import settings
import threading
from AutoDicom.common.dataSort import *
from ..models import stress, stress_record

from AutoDicom.models import duration_record, dicom
from AutoProject.models import dictionary
from AutoProject.utils.graphql.graphql import *
from AutoProject.common.transport import SSHConnection
from AutoProject.common.PostgreSQL import connect_postgres
from ..common.saveResult import ResultStatistics
from ..common.jmeter import JmeterThread

logger = logging.getLogger(__name__)  # 这里使用 __name__ 动态搜索定义的 logger 配置



class SingleThread(threading.Thread):
    def __init__(self, **kwargs):
        threading.Thread.__init__(self)
        self.Flag = True  # 停止标志位
        self.count = 0  # 可用来被外部访问
        self.obj = stress.objects.get(stressid=kwargs["stressid"])
        self.modelID = kwargs["modelID"]
        self.keyword = 'ST' + str(kwargs["stressid"])
        self.server = self.obj.Host.host
        self.thread_num = 4
        self.CountData = []
        self.studyuid = ''
        # 获取计算机名称
        if socket.gethostname() == "biomindqa38":
            self.local_aet = 'QA38'
        else:
            self.local_aet = 'QA120'
        self.full_fn_fake = '{0}/{1}'.format(settings.LOG_PATH, self.keyword)
        if not os.path.exists(self.full_fn_fake):
            os.makedirs(self.full_fn_fake)

    # 混合测试列队
    def QueData(self, model):
        q = queue.Queue()
        dicomObj = dicom.objects.filter(predictor=model,
                                        stressstatus__in=['1', '2'],
                                        status=True).order_by("slicenumber")
        # 补充数据
        if len(dicomObj):
            if int(model) in [9, 12]:
                dicomList = list(dicomObj)
                # 变成{"病种"：（病人对象，病人对象），"病种"：（病人对象，病人对象，...}
                dictsum = {}
                listsum =[]
                for i in dicomList:
                    if dictsum.get(i.slicenumber) is None:
                        sum = set()
                        sum.add(i)
                    else:
                        sum = dictsum.get(i.slicenumber)
                        sum.add(i)
                    dictsum[i.slicenumber] = sum
                for k, v in dictsum.items():
                    copyList = copylist(list(v), int(self.obj.single))
                    listsum = listsum + copyList
                # print(listsum)
            else:
                listSum = copylist(list(dicomObj), int(self.obj.single))
            # 优先查询组
            for j in listSum:
                dcm = 0
                src_folder = str(j.route)
                while src_folder[-1] == '/':
                    src_folder = src_folder[0:-1]
                if not os.path.exists(src_folder):
                    os.system(f"rclone copy oss://qa-test-data/{j.route} {j.route}")
                try:
                    rand_uid = str(get_rand_uid())
                    cur_date = get_date()
                    cur_time = get_time()

                    file_names = os.listdir(src_folder)
                    file_names.sort()
                    for fn in file_names:
                        full_fn = os.path.join(src_folder, fn)
                        full_fn_fake = os.path.join(self.full_fn_fake, f'{dcm}.dcm')
                        if (os.path.splitext(fn)[1] in '.dcm' == False):
                            continue
                        try:
                            try:
                                ds = pydicom.dcmread(full_fn, force=True)
                            except Exception as e:
                                logging.error('errormsg: failed to read file [{0}]'.format(full_fn))
                            try:
                                ds.StudyInstanceUID = self.norm_string(
                                    f'{str(j.studyinstanceuid)}.{rand_uid}', 64)
                                ds.AccessionNumber = self.norm_string(f"{str(ds.AccessionNumber)}_{rand_uid}", 16)

                            except Exception as e:
                                logging.error(
                                    'failed to fake: file[{0}], error[{1}]'.format(full_fn, e))

                            try:
                                ds.SeriesInstanceUID = self.norm_string(f'{str(ds.SeriesInstanceUID)}.{rand_uid}', 64)
                            except Exception as e:
                                logging.error(
                                    'failed to fake seriesinstanceuid: file[{0}], error[{1}]'.format(full_fn, e))
                            try:
                                ds.SOPInstanceUID = self.norm_string(
                                    '{0}.{1}'.format(str(ds.SOPInstanceUID), rand_uid), 64)
                            except Exception as e:
                                logging.error(
                                    'failed to fake sopinstanceuid: file[{0}], error[{1}]'.format(full_fn, e))
                            try:
                                ds.PatientID = self.norm_string('{0}Sn'.format(str(j.patientid)), 24)
                                ds.PatientName = self.norm_string('{0}ST'.format(str(j.diseases)), 24)

                                ds.StudyDate = cur_date
                                ds.StudyTime = cur_time
                                ds.SeriesDate = cur_date
                                ds.SeriesTime = cur_time
                            except Exception as e:
                                logging.error(
                                    'failed to fake sopinstanceuid: file[{0}], error[{1}]'.format(full_fn, e))

                            try:
                                ds.save_as(full_fn_fake)
                            except Exception as e:
                                logging.error('errormsg: failed to save file [{0}] --{1}'.format(full_fn_fake, e))
                            info = {}
                            if dcm == 0:
                                self.studyuid = ds.StudyInstanceUID
                                info = {
                                    "version": self.obj.version,
                                    "studyuid": ds.StudyInstanceUID,
                                    "type": 'DY',
                                    "slicenumber": j.slicenumber,
                                    "images": j.imagecount,
                                    "modelname": j.predictor,
                                    "Stress_id": self.obj.stressid,
                                    "Host_id": self.obj.Host_id
                                }
                            q.put([full_fn_fake, info])
                            dcm = dcm + 1

                        except Exception as e:
                            logging.error("[匿名错误]:{}".format(e))
                            continue
                except Exception as e:
                    logger.error("遍历文件：{}".format(e))
            return q

    # 匿名混合测试
    def run(self):
        if self.modelID:
            self.modelID = self.modelID
        else:
            self.modelID = self.obj.testdata.split(",")
        # 按模型 循环预测
        for i in self.modelID:
            modelName = dictionary.objects.get(id=i).key
            self.obj.teststatus = f"{modelName}Testing"
            self.obj.status = True
            self.obj.save()

            try:
                q = self.QueData(model=i)
                threads = []
                start_date = datetime.datetime.now()
                try:
                    for i in range(self.thread_num):
                        t = threading.Thread(target=self.sync_send_file, args=(q,))
                        # args需要输出的是一个元组，如果只有一个参数，后面加，表示元组，否则会报错
                        t.start()
                        threads.append(t)
                    for t in threads:
                        t.join()
                        time.sleep(1)
                except Exception as e:
                    logger.error("Thread Run Fail：{0}".format(e))
                    continue
                try:
                    self.verification(start_date, i)
                except Exception as e:
                    logger.error("verification：{0}".format(e))
                    continue
            except Exception as e:
                logger.error("Fail：{0}".format(e))
                continue

        jmeter = JmeterThread(stressid= self.obj.stressid)
        jmeter.setDaemon(True)
        jmeter.start()
        self.obj.status = False
        self.obj.teststatus = '测试结束'
        self.obj.save()

    # 验证预测是否结束
    def verification(self, start_date, modelID):
        # 判断 是否全部预测完成
        while True:
            pai_status = connect_postgres(database="orthanc", host=self.obj.Host_id,
                                              sql=f"select pai_status from aistatus where studyuid ='{self.studyuid}'")
            AiStatus = pai_status.to_dict(orient='records')
            if len(AiStatus):
                if AiStatus[0]["pai_status"] in ["1", "2", "3"]:
                    Result = ResultStatistics(
                        stressid=self.obj.stressid,
                        stressType='DY',
                        start_date=start_date.strftime("%Y-%m-%d %H:%M:%S"),
                        end_date=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        modelID=modelID
                    )
                    Result.QueryResults()
                    logger.info(f"biomind restart host:{self.obj.Host.host}, pwd :{self.obj.Host.pwd}")
                    reSsh = SSHConnection(host=self.obj.Host.host, pwd=self.obj.Host.pwd)
                    reSsh.command("nohup sshpass -p {} biomind restart > restart.log 2>&1 &".format(self.obj.Host.pwd))
                    time.sleep(400)
                    logger.info("sleep complete")
                    break
            logger.info("Forecast not completed sleep 300")
            time.sleep(300)

    # 混合测试发送数据
    def sync_send_file(self, q):
        while not q.empty():
            if not os.path.exists(self.full_fn_fake):
                logger.info("break {}".format(testData))
                break
            testData = q.get()
            # 发送数据
            try:
                commands = [
                    "storescu",
                    self.obj.Host.host,
                    self.obj.Host.port,
                    "-aec", self.obj.Host.remarks,
                    "-aet", self.local_aet,
                    testData[0]
                ]
                popen = sp.Popen(commands, stderr=sp.PIPE, stdout=sp.PIPE, shell=False)
                popen.communicate()
                logger.info(f"发送成功 {commands}")
                os.remove(testData[0])
            except Exception as e:
                logging.error('send_file error: {0}'.format(e))
            try:
                if testData[1] != {}:
                    stress_record.objects.create(**testData[1])
            except Exception as e:
                logger.error('[获取数据失败]： [{0}]'.format(e))


    def norm_string(self, str, len_norm):
        str_dest = str
        while len(str_dest) > len_norm or str_dest[0] == '.':
            str_dest = str_dest[1:]
        return str_dest


    def setFlag(self, parm):  # 外部停止线程的操作函数
        if self.obj.jmeterstatus is True:
            stoptest = JmeterThread(stressid=self.obj.stressid)
            # 设为保护线程，主进程结束会关闭线程
            stoptest.setFlag = False
        self.Flag = parm  # boolean
        shutil.rmtree(self.full_fn_fake)

