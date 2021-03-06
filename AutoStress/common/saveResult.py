from django.db import transaction
from django.db.models import Count, Case, When, Sum, Avg, Max, Min
from ..models import stress_result, stress
from ..serializers import stress_result_Deserializer
from AutoDicom.models import duration_record
from AutoDicom.serializers import duration_record_Deserializer, duration_record_Serializer

from AutoProject.common.PostgreSQL import connect_postgres

from AutoProject.models import dictionary
from AutoProject.utils.graphql.graphql import *

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


class ResultStatistics:
    def __init__(self, stressid, stressType, start_date=None, end_date=None, modelID=None):
        self.stressId = stressid
        self.modelID = modelID
        self.obj = stress.objects.get(stressid=self.stressId)
        self.stressType = stressType
        self.start_date = self.obj.start_date if start_date is None else start_date
        self.end_date = self.obj.end_date if end_date is None else end_date

    def QueryResults(self):
        """
          从被测服务器数据库 查询 测试结果
        """
        uids = ''
        # 测试数据查询
        for i in duration_record.objects.filter(relation_id=self.stressId, type=self.stressType):
            uids = uids + '\'' + str(i.studyuid) + '\','

        for j in ['aistatus', 'predictionrecord']:
            try:
                # 查询sql
                sqlOjb = dictionary.objects.get(key=j, type='stresssql', status=True)
                sql = sqlOjb.value.format(self.start_date, self.end_date, uids[:-1])

                # 查询结果
                result = connect_postgres(database="orthanc",
                                          host=self.obj.Host.id,
                                          sql=sql)
                # 循环更新查询结果
                for i in result.to_dict(orient='records'):
                    data = {}
                    if j == "predictionrecord":
                        data = {
                            "sec": str(i["sec"]),
                            "start": str(i["start"]),
                            "end": str(i["end"]),
                            "aistatus": 3,
                            "model": i["model"]
                        }
                    else:
                        data = {
                            "error": str(i["error"]),
                            "aistatus": str(i["aistatus"]),
                            "job_sec": str('%.2f' % (float(i["job_time"]))),
                            "job_start": str(i["job_start"]),
                            "job_end": str(i["job_end"]),
                            "diagnosis": str(i["diagnosis"]),

                        }
                    try:
                        recordObj = duration_record.objects.get(relation_id=self.stressId, studyuid=i["studyuid"], type=self.stressType)
                        serializer = duration_record_Serializer(data=data)
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
        self.SaveResults()

    # def median(self):
    #     data.sort()
    #     half = len(data) // 2
    #     return (data[half] + data[~half]) / 2

    # 保存结果
    def SaveResults(self):
        """
            根据模型 分组查询 stress_record 表
        """
        try:
            if self.modelID is None:
                self.modelID = self.obj.testdata.split(",")
                # 删除 之前数据
                stress_result.objects.filter(Stress=self.stressId, type=self.stressType).delete()
            else:
                self.modelID = [self.modelID]
                stress_result.objects.filter(Stress=self.stressId, type=self.stressType, modelname=self.modelID).delete()
        except:
            logger.error("删除旧的性能结果数据数据失败")

        # 按模型 查询成功失败 数量
        recordObj = duration_record.objects.filter(
            relation_id=self.stressId, type=self.stressType, slicenumber__isnull=True, modelname__in=self.modelID).values("model").annotate(
            count=Count(1),
            ModelAvg=Avg('sec'),
            ModelMax=Max('sec'),
            ModelMin=Min('sec'),
            JobAvg=Avg('job_sec'),
            JobMax=Max('job_sec'),
            JobMin=Min('job_sec'),
            imagesAvg=Avg('image'),
            imagesMax=Max('image'),
            imagesMin=Min('image'),
            success=Count(Case(When(aistatus=3, then=0))),
            warn=Count(Case(When(aistatus=2, then=0))),
            fail=Count(Case(When(aistatus=1, then=0))),
        )
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
                    "version": self.obj.version,
                    "modelname": i["modelname"],
                    "type": self.stressType,
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
                    "Stress_id": self.stressId,
                    "slicenumber": None,
                    "count": i["count"],
                    "start_date": self.start_date,
                    "end_date": self.end_date
                })
            except Exception as e:
                logger.error(e)
                continue
        self.sliceResults()

    def sliceResults(self):
        ObjRecord = duration_record.objects.filter(
            Stress_id=self.stressId, type=self.stressType, slicenumber__isnull=False, model__in=self.modelID).values(
            "slicenumber").annotate(
            count=Count(1),
            ModelAvg=Avg('sec'),
            ModelMax=Max('sec'),
            ModelMin=Min('sec'),
            JobAvg=Avg('job_sec'),
            JobMax=Max('job_sec'),
            JobMin=Min('job_sec'),
            imagesAvg=Avg('image'),
            imagesMax=Max('image'),
            imagesMin=Min('image'),
            success=Count(Case(When(aistatus=3, then=0))),
            warn=Count(Case(When(aistatus=2, then=0))),
            fail=Count(Case(When(aistatus=1, then=0))),
        )

        """
            根据层厚保存到stress_result 表 压测详细数据
        """
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
                try:
                    modelname = duration_record.objects.filter(Stress_id=self.stressId, type=self.stressType, slicenumber=i["slicenumber"])[0]["model"]
                except:
                    modelname = 9

                stress_result.objects.create(**{
                    "version": self.obj.version,
                    "modelname": modelname,
                    "type": self.stressType,
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
                    "Stress_id": self.stressId,
                    "slicenumber": i["slicenumber"],
                    "count": i["count"],
                    "start_date": self.start_date,
                    "end_date": self.end_date
                })
            except Exception as e:
                logger.error(e)
                continue