import datetime
import os
import shutil
import threading
import time

import numpy as np
from django.db import connection
from django.db import transaction
from django.db.models import Count, Case, When, Sum
from django.conf import settings
from ..models import stress_record, stress_result, stress
from ..serializers import stress_result_Deserializer
from .loganalys import errorLogger
from AutoProject.common.PostgreSQL import connect_postgres
from AutoProject.common.regexUtil import csv
from AutoProject.models import Server, dictionary, uploadfile
from AutoProject.utils.graphql.graphql import *
from AutoProject.utils.keycloak.login_kc import login_keycloak
from AutoProject.common.transport import SSHConnection

from AutoDicom.common.dicomBase import checkuid, voteData
from AutoDicom.models import duration_record, dicom
from django.conf import settings

logger = logging.getLogger(__name__)



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

# 保存结果
class ResultThread(threading.Thread):
    def __init__(self, *args, **kwargs):
        threading.Thread.__init__(self)
        self.Flag = True  # 停止标志位
        self.stressid = kwargs["stressid"]
        self.obj = stress.objects.get(stressid=self.stressid)
        self.server = self.obj.Host.host
        self.testdata = self.obj.testdata

    # 测试结果
    def run(self):
        try:
            # 删除 之前数据
            stress_record.objects.filter(Stress=self.stressid).delete()
            stress_result.objects.filter(Stress=self.stressid, type__in=['prediction', 'job']).delete()
        except:
            logger.error("删除旧的性能结果数据数据失败")

        # 模型预测时间 job时间
        for type in ['prediction', 'job']:
            obj = dictionary.objects.get(key=type, status=1, type='stresssql')
            # 测试模型数据查询
            for i in self.testdata.split(","):
                infos = {}
                sql = 'SELECT dr.studyinstanceuid ,d.imagecount,d.slicenumber FROM duration_record dr JOIN dicom d ON dr.studyolduid = d.studyinstanceuid WHERE dr.duration_id = \'0{0}\'AND d.predictor ={1}'.format(
                    str(self.stressid), i)
                cursor = connection.cursor()
                cursor.execute(sql)
                ret = cursor.fetchall()
                # 生成查询数据
                for j in ret:
                    if infos.__contains__(j[2]) is False:
                        infos = {
                            j[2]: {"uids": '\'' + str(j[0]) + '\',',
                                   "image": [j[1]]
                                   }
                        }
                    else:
                        infos[j[2]]["uids"] = infos[j[2]]["uids"] + '\'' + str(j[0]) + '\','
                        infos[j[2]]["image"].append(j[1])
                try:
                    # 循环查询结果
                    for k, v in infos.items():
                        result = connect_postgres(database="orthanc",
                                                  host=self.obj.Host.id,
                                                  sql=obj.value.format(v["uids"][:-1], self.obj.start_date,
                                                                       self.obj.end_date))
                        dict = result.to_dict(orient='records')
                        try:
                            dict[0]["avgimages"], dict[0]["maximages"], dict[0]["minimages"] = str(
                                '%.2f' % np.mean(v["image"])), str(
                                np.max(v["image"])), str(np.min(v["image"]))
                        except:
                            dict[0]["avgimages"], dict[0]["maximages"], dict[0]["minimages"] = None, None, None
                        dict[0]["version"] = self.obj.version
                        dict[0]["modelname"] = i
                        dict[0]["type"] = type
                        dict[0]["slicenumber"] = k
                        dict[0]["Stress"] = self.obj.stressid

                        stressserializer = stress_result_Deserializer(data=dict[0])
                        with transaction.atomic():
                            stressserializer.is_valid()
                            stressserializer.save()
                except Exception as e:
                    logger.error("数据写入失败{}".format(e))
                    continue
        # 保存本次预测详情
        self.SaveRecord()

    def SaveRecord(self):
        # 按模型 查询成功失败 数量
        obj = stress_record.objects.filter(
            Stress_id=self.obj.stressid, modelname__in=self.obj.testdata.split(",")).values("modelname").annotate(
            success=Count(Case(When(aistatus=3, then=0))),
            warn=Count(Case(When(aistatus=2, then=0))),
            fail=Count(Case(When(aistatus=1, then=0))),
        )

        # 循环数据保存
        for i in obj:
            try:
                resultObj = stress_result.objects.get(Stress_id=self.obj.stressid,
                                                      type="prediction",
                                                      modelname=i["modelname"])

                total = i["success"] + i["warn"] + i["fail"]
                resultObj.rate = (i["success"] + i["warn"]) / total * 100
                resultObj.save()
            except Exception as e:
                logger.error(e)
                continue

    # 保存 job 结果数据
    def JobRecord(self):
        # 查询测试时间 job 数据
        for j in ["predictionrecord", "jobmetrics"]:
            sqlobj = dictionary.objects.get(key=j)
            sql = sqlobj.value.format(self.obj.start_date, self.obj.end_date)
            result = connect_postgres(database="orthanc", host=self.obj.Host.id,
                                      sql=sql)
            dict = result.to_dict(orient='records')
            # 循环数据保存
            for i in dict:
                try:
                    drobj = duration_record.objects.get(studyinstanceuid=i["studyuid"])
                    dicomobj = dicom.objects.get(studyinstanceuid=drobj.studyolduid, stressstatus__in=[1,2])
                    data = {
                        "studyuid": i["studyuid"],
                        "job_id": self.server,
                        "start": str(i["start"])[:19],
                        "end": str(i["end"])[:19],
                        "sec": str(i["sec"]),
                        "error": str(i["error"]),
                        "modelname": dicomobj.predictor,
                        "version": self.obj.version,
                        "type": 'job',
                        "aistatus": i["aistatus"],
                        "Stress_id": self.stressid,
                        "images": dicomobj.imagecount,
                        "slicenumber": dicomobj.slicenumber,
                        "type": j
                    }
                    stress_record.objects.create(**data)
                except Exception as e:
                    logger.error(e)
                    continue

    def errorlog(self):
        ssh = SSHConnection(host=self.server, port=22, user=self.obj.Host.user, pwd=self.obj.Host.pwd)
        os.system("rm -rf {}/pm2.zip".format(settings.LOG_PATH))
        downpath = '/home/biomind/.biomind/lib/versions/{}/logs/pm2'.format(self.obj.version)
        ospath = '{}/pm2.zip'.format(settings.LOG_PATH)
        ssh.download(ospath, downpath)
        errorLogger(self.stressid, self.obj.version, ospath)
        ssh.close()

    def setFlag(self, parm):  # 外部停止线程的操作函数
        self.Flag = parm  # boolean

    def setParm(self, parm):  # 外部修改内部信息函数
        self.Parm = parm

    def getParm(self):  # 外部获得内部信息函数
        return self.parm
