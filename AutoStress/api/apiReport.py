from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from AutoProject.models import pid

from rest_framework.authentication import TokenAuthentication
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from AutoProject.common.api_response import JsonResponse
from ..serializers import stress_Deserializer
from ..common.saveResult import *
from ..common.PerformanceResult import *
from AutoDicom.common.dicomBase import baseTransform
from AutoDicom.common.deletepatients import *
from ..common.stressReport import StressReport
from ..common.stressfigure import stressdataFigure
from AutoStress.models import stress

logger = logging.getLogger(__name__)  # 这里使用 __name__ 动态搜索定义的 logger 配置

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
            stressId = int(request.GET.get("stressId", 20))
        except (TypeError, ValueError):
            return JsonResponse(code="999985", msg="必传 stressId!")

        st = StressReport(stressId)
        report = st.report()
        obj = stress.objects.get(stressid=stressId)
        type = request.GET.get("type", "jz")
        checkversion = request.GET.get("checkversion", obj.version)
        model = request.GET.get("model", 1)

        if type == 'jz':
            stresstype = ['predictionJZ', 'jobJZ']
            prediction = stress_result.objects.filter(version=obj.version,
                                                      type__in=['predictionJZ', 'lung_prediction'])
            job = stress_result.objects.filter(version=obj.version, type__in=['jobJZ', 'lung_jobJZ'])

            predictionb = stress_result.objects.filter(version=checkversion,
                                                       type__in=['predictionJZ', 'lung_JZ'])
            jobb = stress_result.objects.filter(version=checkversion, type__in=['jobJZ', 'lung_jobJZ'])
            result = map(dataCheck, [[prediction, predictionb], [job, jobb], [job, prediction]])
        elif type == 'dy':
            stresstype = ['predictiondy', 'jobdy']
            prediction = stress_result.objects.filter(version=obj.version,
                                                      type__in=['predictiondy', 'lung_dy'])
            job = stress_result.objects.filter(version=obj.version, type__in=['jobdy', 'lung_jobdy'])

            predictionb = stress_result.objects.filter(version=checkversion,
                                                       type__in=['predictiondy', 'lung_dy'])
            jobb = stress_result.objects.filter(version=checkversion, type__in=['jobdy', 'lung_jobdy'])

            result = map(dataCheck, [[prediction, predictionb], [job, jobb], [job, prediction]])
        else:
            prediction = stress_result.objects.filter(version=obj.version,
                                                      type__in=['prediction', 'lung_prediction'])
            job = stress_result.objects.filter(version=obj.version, type__in=['job', 'lung_job'])

            predictionb = stress_result.objects.filter(version=checkversion,
                                                       type__in=['prediction', 'lung_prediction'])
            jobb = stress_result.objects.filter(version=checkversion, type__in=['job', 'lung_job'])
            stresstype = ['prediction', 'job']

            result = map(dataCheck, [[prediction, predictionb], [job, jobb], [job, prediction]])
        chartData = {}

        return JsonResponse(data={"report": report,
                                  "predictionresult": result[0],
                                  "jobresult": result[1],
                                  "diffresult": result[2],
                                  "chartData": chartData
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