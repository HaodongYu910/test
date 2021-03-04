import os
from TestPlatform.common.regexUtil import savecsv
from TestPlatform.models import GlobalHost, dicom ,dictionary
from Dicom.common.dicomdetail import checkuid
from ..models import auto_uicase, autoui, auto_uirecord
import datetime
import os
import shutil
import threading
import time
import logging
import numpy as np
from django.db import connection
from django.db import transaction

logger = logging.getLogger(__name__)


class AutoUiThread(threading.Thread):
    def __init__(self, *args, **kwargs):
        threading.Thread.__init__(self)
        self.Flag = True  # 停止标志位
        # self.count = kwargs["count"]  # 可用来被外部访问的
        # 性能测试id
        self.autoid = kwargs["autoid"]
        self.obj = autoui.objects.get(autoid=self.autoid)
        self.Hostobj = GlobalHost.objects.get(id=self.obj.hostid)
        self.server = self.Hostobj.host
        # self.kc =

    #  UI 测试
    def Uitest(self):
        self.obj.starttime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            obj = auto_uirecord.objects.filter(autoid=self.autoid)
            for i in obj:
                checkuid(self.obj.hostid, self.server, str(i.dicomid))
                # delreport(login_keycloak(self.obj.hostid), str(i.studyuid))

        except Exception as e:
            logger.error("执行预测基准测试数据失败：{0}".format(e))
        self.obj.status = True
        self.obj.save()
        #  UI 测试

    def UiStop(self):
        self.obj.completiontime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            print("测试")
        except Exception as e:
            logger.error("执行预测基准测试数据失败：{0}".format(e))
        self.obj.status = False
        self.obj.save()

    # 创建ui测试任务数据
    def addUitest(self):
        try:
            for i in self.obj.cases.split(","):
                caseobj = auto_uicase.objects.get(caseid=i)
                for j in caseobj.testdata.split(","):
                    for k in dicom.objects.filter(fileid=j):
                        try:
                            vote = k.vote.replace('{', '{"')
                            vote = vote.replace(',', ',"')
                            vote = vote.replace(':', '":')
                            vote = vote.replace(',"}', '}')
                            try:
                                dictionaryobj = dictionary.objects.get(key=k.diagnosis,type="diseases",status=True)
                                diagnosis = dictionaryobj.value
                            except:
                                diagnosis = k.diagnosis
                            data = {
                                "dicomid": k.id,
                                "studyuid": k.studyinstanceuid,
                                "vote": vote,
                                "expect": diagnosis,
                                "server": self.server,
                                "caseid": int(i),
                                "autoid": self.autoid,
                                "status": False
                            }
                            auto_uirecord.objects.create(**data)
                        except Exception as e:
                            continue
                            logger.error("测试添加失败：{0}".format(e))
        except Exception as e:
            logger.error("测试添加失败：{0}".format(e))

    # 测试结果
    def SaveResult(self):
        try:
            return 1
        except Exception as e:
            logger.error("数据写入失败{}".format(e))

    def setFlag(self, parm):  # 外部停止线程的操作函数
        self.Flag = parm  # boolean


    def setParm(self, parm):  # 外部修改内部信息函数
        self.Parm = parm


    def getParm(self):  # 外部获得内部信息函数
        return self.parm
