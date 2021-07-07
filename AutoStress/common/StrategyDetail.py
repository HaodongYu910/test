from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db import transaction
from django.db.models import Count, Case, When

from rest_framework.authentication import TokenAuthentication
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView

from AutoProject.common.api_response import JsonResponse
from ..serializers import stress_jmeter_Serializer, stress_result_Deserializer

from AutoDicom.common.dicomBase import baseTransform

from AutoProject.models import dictionary

from ..models import stress, stress_record, stress_result, stress_jmeter
import datetime
import logging

logger = logging.getLogger(__name__)  # 这里使用 __name__ 动态搜索定义的 logger 配置


def ForecastNo(**kwargs):

    stressId = kwargs["stressId"]
    strategy = kwargs["strategy"]
    try:
        listObj = list(stress_result.objects.filter(Stress_id=stressId, type=strategy).order_by("-start_date"))
        StartDate = listObj[-1].start_date
        EndDate = listObj[0].end_date
    except:
        StartDate = ""
        EndDate = ""

    if strategy in ["HH", "DY"]:
        aiObj = stress_record.objects.filter(
            Stress_id=stressId, type=strategy).values('Stress_id').annotate(
            total=Count(1),
            success=Count(Case(When(aistatus=3, then=0))),
            warn=Count(Case(When(aistatus=2, then=0))),
            fail=Count(Case(When(aistatus=1, then=0))),
        )
        if not aiObj:
            total = 0
            success = 0
            fail = 0
        else:
            total = aiObj[0]["success"] + aiObj[0]["warn"] + aiObj[0]["fail"]
            success = aiObj[0]["success"] + aiObj[0]["warn"]
            fail = aiObj[0]["fail"]

        # 全部成功失败个数
        return {
            "total": total,
            "success": success,
            "fail": fail,
            "StartDate": StartDate,
            "EndDate": EndDate
        }
    else:
         return {
             "StartDate": StartDate,
             "EndDate": EndDate
         }


# 返回模型预测结果列表
def ModelList(**kwargs):
    stressId = kwargs["stressId"]
    strategy = kwargs["strategy"]
    obj = stress.objects.get(stressid=stressId)
    resultObj = stress_result.objects.filter(Stress_id=stressId, type=strategy)
    testData = obj.testdata.split(",")

    if len(resultObj) == 0:
        modelDetail = []
    else:
        serializer = stress_result_Deserializer(resultObj, many=True)
        for i in serializer.data:
            i["modelId"] = i["modelname"]
            i["modelname"] = dictionary.objects.get(id=i["modelname"]).key
        modelDetail = serializer.data
    try:
        for j in resultObj:
            testData.remove(j.modelname)
    except Exception as e:
        logger.error(e)
    for k in testData:
        modelDetail.append({
            "modelId": k,
            "modelname": dictionary.objects.get(id=k).key,
            "type": "HH",
            "start_date": "--",
            "end_date": "--"
        })
    return modelDetail

def JmeterData(**kwargs):
    """
        stressId: 性能测试id
        strategy: 页面 类型
        progress: 进度信息
        statistics： 成功失败信息
        JmeterData ： jmeter列表

    """
    stressId = kwargs["stressId"]
    strategy = kwargs["strategy"]

    # 返回 jmeter
    try:
        obj = stress_jmeter.objects.filter(Stress_id=stressId, status=True)
        serializer = stress_jmeter_Serializer(obj, many=True)
    except Exception as e:
        logger.error(f"Jmeter info error: {e}")
        return {}
    return serializer.data

def strategyList(**kwargs):
    """
        stressId: 性能测试id
        strategy: 页面 类型
        progress: 进度信息
        statistics： 成功失败信息
        JmeterData ： jmeter列表

    """
    stressId = kwargs["stressId"]
    strategy = kwargs["strategy"]
    progress = {}
    statistics = {}
    obj = stress.objects.get(stressid=stressId)

    # 判断加载tab 页面 根据加载返回数据
    if strategy == "SceneConfiguration":
        total = int(len(obj.testdata.split(",")))
        try:
            manual = float(stress_result.objects.filter(Stress_id=stressId, type="JZ").count() / total)
            single = float(stress_result.objects.filter(Stress_id=stressId, type="DY").count() / total)
        except Exception as e:
            logger.error(e)

        try:
            now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            if obj.start_date is None:
                hybrid = 0
            elif obj.end_date <= now:
                hybrid = 1
            else:
                start = datetime.datetime.strptime(obj.start_date, '%Y-%m-%d %H:%M:%S')
                durationTime = float(obj.duration * 3600)
                hybrid = float((datetime.datetime.now() - start).seconds / durationTime)
        except Exception as e:
            logger.error(e)

        # 返回进度
        progress = {
            "manual": '%.2f' % (manual * 100),
            "single": '%.2f' % (single * 100),
            "hybrid": '%.2f' % (hybrid * 100)
        }
    else:
        statistics = ForecastNo(stressId=stressId, strategy=strategy),
    DataDist = {
        "modelDetail": ModelList(stressId=stressId, strategy=strategy),
        "progress": progress,
        "statistics": statistics,
        "JmeterData": JmeterData(stressId=stressId, strategy=strategy)
    }
    return DataDist