from django.db import transaction
from django.db.models import Count, Case, When, Sum, Avg, Max, Min
from ..models import stress_record, stress_result, stress
from ..serializers import stress_result_Deserializer, stress_record_Deserializer
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
    def __init__(self, stressid, stressType, start_date=None, end_date=None):
        self.stressId = stressid
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
        for i in stress_record.objects.filter(Stress_id=self.stressId, type=self.stressType):
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
                    if j == "predictionrecord":
                        data = {}
                        data = {
                            "sec": str(i["sec"]),
                            "start": str(i["start"])[:19],
                            "end": str(i["end"])[:19],
                            "aistatus": 3
                        }
                    else:
                        data = {
                            "error": str(i["error"]),
                            "aistatus": str(i["aistatus"]),
                            "job_time": str('%.2f' % (float(i["job_time"]))),
                            "job_end": str(i["job_end"])[:19]

                        }
                    try:
                        recordObj = stress_record.objects.get(Stress_id=self.stressId, studyuid=i["studyuid"])
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
        self.SaveResults()

    # 保存结果
    def SaveResults(self):
        """
            根据模型 分组查询 stress_record 表
        """
        try:
            # 删除 之前数据
            stress_result.objects.filter(Stress=self.stressId, type=self.stressType).delete()
        except:
            logger.error("删除旧的性能结果数据数据失败")

        # 按模型 查询成功失败 数量
        recordObj = stress_record.objects.filter(
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
        self.SaveResult(recordObj, modelname=1)

        ObjRecord = stress_record.objects.filter(
            Stress_id=self.stressId, type=self.stressType, slicenumber__isnull=False).values(
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
        self.SaveResult(ObjRecord, slicenumber=1)

    def SaveResult(self, obj, modelname=None, slicenumber=None):
        """
            根据模型 保存到stress_result 表 压测详细数据
        """
        # 循环数据保存
        for i in obj:
            if slicenumber is not None:
                slicenumber = i["slicenumber"]

            elif modelname is not None:
                modelname = i["modelname"]
                "".split(",")
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
                    "slicenumber": slicenumber,
                    "count": i["count"],
                    "start_date": self.start_date,
                    "end_date": self.end_date
                })
            except Exception as e:
                logger.error(e)
                continue