import time
import datetime
import threading
import shutil
import os
from AutoDicom.common.dataSort import *
from ..common.jmeter import JmeterThread

from AutoDicom.common.queList import QueData, HybridDicom, singleDicom
from AutoDicom.common.DicomSend import SendThread

from django.conf import settings

from django.conf import settings
from ..models import stress_record, stress_result, stress

from AutoProject.utils.graphql.graphql import *
from AutoProject.models import dictionary
from ..common.manual import ManualThread
from AutoProject.common.transport import SSHConnection
from AutoProject.common.PostgreSQL import connect_postgres
from ..common.saveResult import ResultStatistics

logger = logging.getLogger(__name__)  # 这里使用 __name__ 动态搜索定义的 logger 配置


# 性能测试
class StressTest(threading.Thread):
    def __init__(self, stressID, Type, modelID=''):
        threading.Thread.__init__(self)
        self.Flag = True
        self.Type = Type
        self.id = stressID
        self.modelID = modelID
        self.obj = stress.objects.get(stressid=self.id)
        self.full_fn_fake = f'{settings.LOG_PATH}/ST{self.id}'
        if not os.path.exists(self.full_fn_fake):
            os.makedirs(self.full_fn_fake)

    def run(self):
        if self.Flag is True and self.Type in ["JZ", "test"]:
            logger.info('-----------------------------基准测试开始-----------------------------')
            self.Manual()
        elif self.Flag is True and self.Type in ["HH", "test"]:
            logger.info('-----------------------------混合测试开始-----------------------------')
            self.Hybrid()
        elif self.Flag is True and self.Type in ["DY", "test"]:
            logger.info('-----------------------------单一测试开始-----------------------------')
            self.Single()

    def Manual(self):
        try:
            Manual = ManualThread(stressid=self.id, modelID=self.modelID)
            Manual.setDaemon(True)
            Manual.run()
            self.restart()
            time.sleep(300)
        except Exception as e:
            logger.error("基准测试失败：{}".format(e))

    def Hybrid(self):
        try:
            # 开始时间
            self.obj.start_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            # 结束时间
            self.obj.end_date = (
                    datetime.datetime.now() + datetime.timedelta(hours=int(self.obj.duration))).strftime(
                "%Y-%m-%d %H:%M:%S")
            self.obj.teststatus = '混合测试中'
            self.obj.save()
        except Exception as e:
            logger.error(f"更新stress 表 数据失败:{e}")

        if self.obj.jmeterstatus is True:
            logger.info('-----------------------------jmeter 测试开始-----------------------------')
            jmeter = JmeterThread(stressid=self.id)
            jmeter.setDaemon(True)
            jmeter.start()

        try:
            # 预计发送数量
            count = int(self.obj.duration) * 60
            DicomList = HybridDicom(self.obj.testdata.split(","), count)
            logger.info(f"Hybrid dicom list:{len(DicomList)}")
        except Exception as e:
            logger.error(f"Hybrid dicom list fail: {e}")
            return False

        self.Send(DicomList, "HH")

        end_date = int(time.time()) + int(self.obj.duration)*3600
        while True:
            if int(time.time()) >= int(end_date):
                shutil.rmtree(self.full_fn_fake)
                self.restart()
                break

    def Single(self):
        try:
            if self.modelID:
                self.modelID = self.modelID
            else:
                self.modelID = self.obj.testdata.split(",")
            # 按模型 循环预测
            for i in self.modelID:
                # 判断匿名存储文件夹是否存在
                if not os.path.exists(self.full_fn_fake):
                    os.makedirs(self.full_fn_fake)
                modelName = dictionary.objects.get(id=i).key
                self.obj.teststatus = f"{modelName}Testing"
                self.obj.save()
                count = int(self.obj.single) * 100
                DicomList = singleDicom(i, count)
                start_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                self.Send(DicomList, 'DY')
                end_date = int(time.time()) + int(self.obj.single) * 3600
                while True:
                    if int(time.time()) >= int(end_date):
                        shutil.rmtree(self.full_fn_fake)
                        try:
                            Result = ResultStatistics(
                                stressid=self.id,
                                stressType='DY',
                                start_date=start_date,
                                end_date=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                modelID=i
                            )
                            Result.QueryResults()
                        except Exception as e:
                            logger.error(f"单一测试保存结果失败 ：{e}")
                        self.restart()
                        break

            if self.obj.jmeterstatus is True:
                logger.info('-----------------------------jmeter 测试开始-----------------------------')
                jmeter = JmeterThread(stressid=self.id)
                jmeter.setDaemon(True)
                jmeter.start()
        except Exception as e:
            logger.error("单一测试失败：{}".format(e))

    def Send(self, DicomList, Type):
        logger.info('-----------------------------生成队列-----------------------------')
        try:
            que = QueData(
                relation_id=self.id,
                Host_id=self.obj.Host_id,
                Type=Type,
                DicomList=DicomList,
                full_fn_fake=self.full_fn_fake,
                patientID=f"{Type}st",
                patientName=f"{Type}ST"
            )
        except Exception as e:
            logger.error(f"QueData fail: {e}")

        try:
            ST = SendThread(
                q=que,
                hostID=self.obj.Host_id,
                anonymous=True,
                full_fn_fake=self.full_fn_fake,
                stop=[0, self.id]
            )
            ST.setDaemon(True)
            ST.start()
        except Exception as e:
            logger.error(f"SendThread fail: {e}")

    # # 验证预测是否结束
    # def verification(self, start_date, modelID):
    #         # 判断 是否全部预测完成
    #         a = 0
    #         while True:
    #             pai_status = connect_postgres(database="orthanc", host=self.obj.Host_id,
    #                                           sql=f"select pai_status from aistatus where studyuid ='{self.studyuid}'")
    #             AiStatus = pai_status.to_dict(orient='records')
    #             if len(AiStatus):
    #                 if AiStatus[0]["pai_status"] in ["1", "2", "3"]:
    #                     Result = ResultStatistics(
    #                         stressid=self.obj.stressid,
    #                         stressType='DY',
    #                         start_date=start_date.strftime("%Y-%m-%d %H:%M:%S"),
    #                         end_date=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    #                         modelID=modelID
    #                     )
    #                     Result.QueryResults()
    #                     logger.info(f"biomind restart host:{self.obj.Host.host}, pwd :{self.obj.Host.pwd}")
    #                     reSsh = SSHConnection(host=self.obj.Host.host, pwd=self.obj.Host.pwd)
    #                     reSsh.command(
    #                         "nohup sshpass -p {} biomind restart > restart.log 2>&1 &".format(self.obj.Host.pwd))
    #                     time.sleep(400)
    #                     logger.info("sleep complete")
    #                     break
    #             elif a > 24:
    #                 Result = ResultStatistics(
    #                     stressid=self.obj.stressid,
    #                     stressType='DY',
    #                     start_date=start_date.strftime("%Y-%m-%d %H:%M:%S"),
    #                     end_date=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    #                     modelID=modelID
    #                 )
    #                 Result.QueryResults()
    #                 logger.info(f"biomind restart host:{self.obj.Host.host}, pwd :{self.obj.Host.pwd}")
    #                 reSsh = SSHConnection(host=self.obj.Host.host, pwd=self.obj.Host.pwd)
    #                 reSsh.command("nohup sshpass -p {} biomind restart > restart.log 2>&1 &".format(self.obj.Host.pwd))
    #                 time.sleep(400)
    #                 logger.info
    #
    #             logger.info("Forecast not completed sleep 300")
    #             time.sleep(300)
    #             a = a + 1
    # 重启服务器
    def restart(self):
        try:
            ssh = SSHConnection(host=self.obj.Host.host, pwd=self.obj.Host.pwd)
            logger.info("Server:{}：重启服务".format(self.obj.Host.host))
            ssh.command(f"nohup sshpass -p {self.obj.Host.pwd} biomind restart &")
            time.sleep(500)
            ssh.close()
        except Exception as e:
            logger.error("Server::{0}：重启服务失败----失败原因：{1}".format(self.obj.Host.host, e))

    def stop(self, parm=False):  # 外部停止线程的操作函数
        self.Flag = parm  # boolean
        shutil.rmtree(self.full_fn_fake)
        self.obj.status = False
        self.obj.teststatus = "停止"
        self.obj.save()
