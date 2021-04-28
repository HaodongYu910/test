import datetime
import os
import shutil
import threading
import time

import numpy as np
from django.db import connection
from django.db import transaction
from django.db.models import Count, Case, When, Sum, Avg, Max, Min
from django.conf import settings
from ..models import stress_record, stress_result, stress
from ..serializers import stress_result_Deserializer, stress_record_Deserializer
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
        self.stressType = kwargs["stressType"]
        self.obj = stress.objects.get(stressid=self.stressid)
        self.server = self.obj.Host.host

    # 测试结果
    def run(self):
        uids = ','
        # 测试数据查询
        for i in stress_record.objects.filter(Stress_id=self.stressid, type=self.stressType):
            uids = uids + '\'' + str(i.studyuid) + '\','

        for j in ['aistatus', 'jobmetrics', 'predictionrecord']:
            try:
                # 查询sql
                sqlOjb = dictionary.objects.get(key=j, type='stresssql', status=True)
                sql = sqlOjb.value.format(self.obj.start_date, self.obj.end_date, uids[:-1])

                # 查询结果
                result = connect_postgres(database="orthanc",
                                          host=self.obj.Host.id,
                                          sql=sql)
                dict = result.to_dict(orient='records')
                # 循环更新查询结果
                for i in dict:
                    try:
                        recordObj = stress_record.objects.get(Stress_id=self.stressid, studyuid=i["studyuid"])
                        serializer = stress_record_Deserializer(data=i)
                        with transaction.atomic():
                            if serializer.is_valid():
                                # 修改数据
                                serializer.update(instance=recordObj, validated_data=i)
                    except Exception as e:
                        logger.error("数据写入失败{}".format(e))
                        continue
            except Exception as e:
                logger.error("查询数据失败{}".format(e))
                continue

        # 保存本次预测详情
        self.SaveResult()

    def SaveResult(self):
        # try:
        #     # 删除 之前数据
        #     stress_result.objects.filter(Stress=self.stressid, type__in=['hh', '']).delete()
        # except:
        #     logger.error("删除旧的性能结果数据数据失败")

        # 按模型 查询成功失败 数量
        obj = stress_record.objects.filter(
            Stress_id=self.obj.stressid, type=self.stressType, slicenumber__isnull=True).values("modelname").annotate(
            count=Count(1),
            ModelAvg=Avg('sec'),
            ModelMax=Max('sec'),
            ModelMin=Min('sec'),
            JobAvg=Avg('job_time'),
            JobMax=Max('job_time'),
            JobMin=Min('job_time'),
            imagesAvg=Avg('images'),
            imagesMax=Max('images'),
            imagesMin=Min('images'),
            success=Count(Case(When(aistatus=3, then=0))),
            warn=Count(Case(When(aistatus=2, then=0))),
            fail=Count(Case(When(aistatus=1, then=0))),
        )

        # 循环数据保存
        for i in obj:
            try:
                total = i["success"] + i["warn"] + i["fail"]
                rate = (i["success"] + i["warn"]) / total * 100

                data = {
                    "version": self.obj.version,
                    "modelname": i["modelname"],
                    "type": self.stressType,
                    "avg": i["ModelAvg"],
                    "min": i["ModelMin"],
                    "max": str(i["ModelMax"]),
                    "jobavg": str(i["JobAvg"]),
                    "jobmin": i["JobMin"],
                    "jobmax": i["JobMax"],
                    "rate": rate,
                    "minimages": i["imagesMin"],
                    "maximages": i["imagesMax"],
                    "avgimages": i["imagesAvg"],
                    "Stress_id": self.stressid,
                    "slicenumber": None,
                    "count": i["count"]
                }
                stress_result.objects.create(**data)
            except Exception as e:
                logger.error(e)
                continue
                # 按模型 查询成功失败 数量
            obj = stress_record.objects.filter(
                    Stress_id=self.obj.stressid, type=self.stressType, slicenumber__isnull=False).values(
                    "slicenumber").annotate(
                    count=Count(1),
                    ModelAvg=Avg('sec'),
                    ModelMax=Max('sec'),
                    ModelMin=Min('sec'),
                    JobAvg=Avg('job_time'),
                    JobMax=Max('job_time'),
                    JobMin=Min('job_time'),
                    imagesAvg=Avg('images'),
                    imagesMax=Max('images'),
                    imagesMin=Min('images'),
                    success=Count(Case(When(aistatus=3, then=0))),
                    warn=Count(Case(When(aistatus=2, then=0))),
                    fail=Count(Case(When(aistatus=1, then=0))),
                )
            # 循环数据保存
            for i in obj:
                try:
                    total = i["success"] + i["warn"] + i["fail"]
                    rate = (i["success"] + i["warn"]) / total * 100

                    data = {
                            "version": self.obj.version,
                            "modelname": None,
                            "type": self.stressType,
                            "avg": i["ModelAvg"],
                            "min": i["ModelMin"],
                            "max": str(i["ModelMax"]),
                            "jobavg": str(i["JobAvg"]),
                            "jobmin": i["JobMin"],
                            "jobmax": i["JobMax"],
                            "rate": rate,
                            "minimages": i["imagesMin"],
                            "maximages": i["imagesMax"],
                            "avgimages": i["imagesAvg"],
                            "Stress_id": self.stressid,
                            "slicenumber": i["slicenumber"],
                            "count": i["count"]
                        }
                    stress_result.objects.create(**data)
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
