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


# 测试结果统计 保存结果
def ResultStatistics(stressid='', stressType ='HH', start_date=None, end_date=None):
    obj = stress.objects.get(stressid=stressid)
    server = obj.Host.host
    uids = ''
    # 测试数据查询
    for i in stress_record.objects.filter(Stress_id=stressid, type=stressType):
        uids = uids + '\'' + str(i.studyuid) + '\','

    for j in ['aistatus', 'jobmetrics', 'predictionrecord']:
        try:
            # 查询sql
            sqlOjb = dictionary.objects.get(key=j, type='stresssql', status=True)
            sql = sqlOjb.value.format(obj.start_date, obj.end_date, uids[:-1])

            # 查询结果
            result = connect_postgres(database="orthanc",
                                      host=obj.Host.id,
                                      sql=sql)
            # 循环更新查询结果
            for i in result.to_dict(orient='records'):
                if j == "predictionrecord":
                    data = {}
                    data = {
                        "sec": str(i["sec"]),
                        "start": str(i["start"])[:19],
                        "end": str(i["end"])[:19],
                        "aistatus": 3
                    }
                elif j == "jobmetrics":
                    data = {
                        "job_time": str(i["job_time"]),
                        "start": str(i["job_start"])[:19],
                        "end": str(i["job_end"])[:19]
                    }
                else:
                    data = i
                try:
                    recordObj = stress_record.objects.get(Stress_id=stressid, studyuid=i["studyuid"])
                    serializer = stress_record_Deserializer(data=data)
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

    # 保存本次预测详
    try:
        # 删除 之前数据
        stress_result.objects.filter(Stress=stressid, type=stressType).delete()
    except:
        logger.error("删除旧的性能结果数据数据失败")

    # 按模型 查询成功失败 数量
    recordObj = stress_record.objects.filter(
        Stress_id=obj.stressid, type=stressType, slicenumber__isnull=True).values("modelname").annotate(
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
    for i in recordObj:
        try:
            total = i["success"] + i["warn"] + i["fail"]

            ModelAvg = 0 if i["ModelAvg"] is None else '%.2f' % (float(i["ModelAvg"]))
            ModelMin = 0 if i["ModelMin"] is None else '%.2f' % (float(i["ModelMin"]))
            ModelMax = 0 if i["ModelMax"] is None else '%.2f' % (float(str(i["ModelMax"])))
            JobAvg = 0 if i["JobAvg"] is None else '%.2f' % (float(i["JobAvg"]))
            JobMin = 0 if i["JobMin"] is None else '%.2f' % (float(i["JobMin"]))
            JobMax = 0 if i["JobMax"] is None else '%.2f' % (float(i["JobMax"]))
            rate = 0 if i["success"] is None else '%.2f' % (float((i["success"] + i["warn"]) / total * 100))
            imagesMin = 0 if i["imagesMin"] is None else '%.2f' % (float(i["imagesMin"]))
            imagesMax = 0 if i["imagesMax"] is None else '%.2f' % (float(i["imagesMax"]))
            imagesAvg = 0 if i["imagesAvg"] is None else '%.2f' % (float(i["imagesAvg"]))

            stress_result.objects.create(**{
                "version": obj.version,
                "modelname": i["modelname"],
                "type": stressType,
                "avg": ModelAvg,
                "min": ModelMin,
                "max": ModelMax,
                "jobavg": JobAvg,
                "jobmin": JobMin,
                "jobmax": JobMax,
                "rate": rate,
                "minimages": imagesMin,
                "maximages": imagesMax,
                "avgimages": imagesAvg,
                "Stress_id": stressid,
                "slicenumber": None,
                "count": i["count"]
            })
        except Exception as e:
            logger.error(e)
            continue
            # 按模型 查询成功失败 数量
    ObjRecord = stress_record.objects.filter(
        Stress_id=obj.stressid, type=stressType, slicenumber__isnull=False).values(
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
    for i in ObjRecord:
        try:
            total = i["success"] + i["warn"] + i["fail"]
            ModelAvg = 0 if i["ModelAvg"] is None else '%.2f' % (float(i["ModelAvg"]))
            ModelMin = 0 if i["ModelMin"] is None else '%.2f' % (float(i["ModelMin"]))
            ModelMax = 0 if i["ModelMax"] is None else '%.2f' % (float(str(i["ModelMax"])))
            JobAvg = 0 if i["JobAvg"] is None else '%.2f' % (float(i["JobAvg"]))
            JobMin = 0 if i["JobMin"] is None else '%.2f' % (float(i["JobMin"]))
            JobMax = 0 if i["JobMax"] is None else '%.2f' % (float(i["JobMax"]))
            rate = 0 if i["success"] is None else '%.2f' % (float((i["success"] + i["warn"]) / total * 100))
            imagesMin = 0 if i["imagesMin"] is None else '%.2f' % (float(i["imagesMin"]))
            imagesMax = 0 if i["imagesMax"] is None else '%.2f' % (float(i["imagesMax"]))
            imagesAvg = 0 if i["imagesAvg"] is None else '%.2f' % (float(i["imagesAvg"]))

            stress_result.objects.create(**{
                "version": obj.version,
                "modelname": None,
                "type": stressType,
                "avg": ModelAvg,
                "min": ModelMin,
                "max": ModelMax,
                "jobavg": JobAvg,
                "jobmin": JobMin,
                "jobmax": JobMax,
                "rate": rate,
                "minimages": imagesMin,
                "maximages": imagesMax,
                "avgimages": imagesAvg,
                "Stress_id": stressid,
                "slicenumber": i["slicenumber"],
                "count": i["count"],
                "start_date": start_date,
                "end_date": end_date
            })
        except Exception as e:
            logger.error(e)
            continue
