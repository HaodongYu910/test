import datetime
import os
import shutil
import threading
import time

import numpy as np
from django.db import connection
from django.db import transaction
from django.conf import settings
from ..models import stress_record, stress_result, stress
from ..serializers import stress_result_Deserializer
from .loganalys import errorLogger
from AutoTest.common.PostgreSQL import connect_postgres
from AutoTest.common.regexUtil import csv
from AutoTest.models import Server, dictionary, uploadfile
from AutoTest.utils.graphql.graphql import *
from AutoTest.utils.keycloak.login_kc import login_keycloak
from AutoTest.common.transport import SSHConnection

from AutoDicom.common.dicomBase import checkuid, voteData
from AutoDicom.models import duration_record, dicom
from django.conf import settings

logger = logging.getLogger(__name__)


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


# 性能测试
class ManualThread(threading.Thread):
    def __init__(self, *args, **kwargs):
        threading.Thread.__init__(self)
        self.Flag = True  # 停止标志位
        # self.count = kwargs["count"]  # 可用来被外部访问的
        # 性能测试id
        self.stressid = kwargs["stressid"]
        self.obj = stress.objects.get(stressid=self.stressid)
        self.server = self.obj.Host.host
        self.testdata = self.obj.testdata
        self.kc = login_keycloak(self.obj.Host_id)

    #  基准测试
    def run(self):
        self.obj.status = True
        self.obj.teststatus = "基准测试开始"
        self.obj.save()
        try:
            resultobj = stress_result.objects.filter(Stress=self.stressid,
                                                     type__in=['jobJZ', 'predictionJZ', 'lung_jobJZ', 'lung_job'])
            resultobj.delete()
        except:
            logger.error("性能基准数据删除失败")
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
            self.obj.teststatus = "基准测试完成"
            self.obj.save()
        except Exception as e:
            logger.error("执行预测基准测试数据失败：{0}".format(e))


    def setFlag(self, parm):  # 外部停止线程的操作函数
        self.Flag = parm  # boolean

    def setParm(self, parm):  # 外部修改内部信息函数
        self.Parm = parm

    def getParm(self):  # 外部获得内部信息函数
        return self.parm
