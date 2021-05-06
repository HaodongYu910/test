from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from AutoProject.models import pid

from rest_framework.authentication import TokenAuthentication
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from AutoProject.common.api_response import JsonResponse
from ..serializers import stress_Deserializer
from ..common.PerformanceResult import *
from AutoDicom.common.dicomBase import baseTransform
from AutoDicom.common.deletepatients import *
from ..common.stressReport import StressReport
from ..common.stressfigure import stressdataFigure
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
            ChartType = request.GET.get("type", "jz")
            checkversion = request.GET.get("checkversion", obj.version)
            models = ["", str(request.GET.get("models", "1")).strip()]
        except (TypeError, ValueError):
            return JsonResponse(code="999985", msg="必传 stressId!")
        dictObj = dictionary.objects.get(id=models[1])
        st = StressReport(stressId)
        report = st.report()
        result, chartData, LineData = st.ChartData(ChartType=ChartType,
                                                   models=models,
                                                   version=checkversion)
        return JsonResponse(data={"report": report,
                                  "result": result,
                                  "chartData": chartData,
                                  "LineData": LineData,
                                  "modelsName": dictObj.value
                                  }, code="0", msg="成功")


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
