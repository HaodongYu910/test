from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from rest_framework.authentication import TokenAuthentication
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from AutoProject.common.api_response import JsonResponse
from ..serializers import stress_Deserializer

from AutoDicom.common.deletepatients import *
from ..common.stressReport import StressReport
from AutoStress.models import stress

logger = logging.getLogger(__name__)  # 这里使用 __name__ 动态搜索定义的 logger 配置


# 获取性能测试版本号
class stressVersion(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def get(self, request):
        """
        获取性能测试版本
        :param request:
        :return:
        """
        name = request.GET.get("projectName", '晨曦')
        obj = stress.objects.filter(projectname=name).order_by("-version")
        serialize = stress_Deserializer(obj, many=True)
        return JsonResponse(data={"data": serialize.data
                                  }, code="0", msg="成功")

# 获取压测列表
class stressReport(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def get(self, request):
        """
        获取性能列表数据
        :param request:
        :return:
        """
        try:
            stressId = int(request.GET.get("stressId"))
            obj = stress.objects.get(stressid=stressId)
            ChartType = request.GET.get("type", "JZ")
            checkversion = request.GET.get("checkversion", obj.version)
            models = ["", str(request.GET.get("models", "1")).strip()]
        except (TypeError, ValueError):
            return JsonResponse(code="999985", msg="必传 stressId!")
        # 报告信息
        st = StressReport(stressId, ChartType)
        report = st.report()

        # 返回各个版本折线图表 数据
        try:
            chartData = st.ChartData(model=models)
        except Exception as e:
            logger.error("chartData fail:{}".format(e))
            chartData = []

        # 返回 预测时间 折线图
        try:
            LineData = st.recordLine(models[1])
        except Exception as e:
            logger.error("LineData fail:{}".format(e))
            LineData = []
        # 判断是否相同版本 返回 预测 版本比较数据
        try:
            result = st.dataCheck(CheckVersion=checkversion)
        except Exception as e:
            logger.error("resultData fail:{}".format(e))
            result = []

        return JsonResponse(
            data={"report": report,
                  "result": result,
                  "chartData": chartData,
                  "LineData": LineData,
                  "modelsName": dictionary.objects.get(id=models[1]).value
                  },
            code="0",
            msg="成功")


class SaveAnalysis(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def parameter_check(self, data):
        """
        验证参数
        :param data:
        :return:
        """
        try:
            # 必传参数 stressid
            if not data["stressid"] or not data["summary"]:
                return JsonResponse(code="999996", msg="参数有误,必传参数 stressid summary！")

        except KeyError:
            return JsonResponse(code="999996", msg="参数有误,必传参数 stressid summary！！")

    def post(self, request):
        """
            保存总结
            :param request:
            :return:
        """
        data = JSONParser().parse(request)
        result = self.parameter_check(data)
        if result:
            return result
        try:
            obj = stress.objects.get(stressid=data["stressid"])
            serializer = stress_Deserializer(data=data)
            with transaction.atomic():
                if serializer.is_valid():
                    # 修改数据
                    serializer.update(instance=obj, validated_data=data)
            return JsonResponse(code="0", msg="成功")
        except ObjectDoesNotExist:
            return JsonResponse(code="999995", msg="数据不存在！")
