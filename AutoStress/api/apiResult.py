
from rest_framework.authentication import TokenAuthentication
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
import logging
from AutoTest.common.api_response import JsonResponse
from ..common.stress import *
from ..common.PerformanceResult import *
from ..common.stressfigure import stressdataFigure

logger = logging.getLogger(__name__)  # 这里使用 __name__ 动态搜索定义的 logger 配置


class stressResult(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def parameter_check(self, data):
        """
        验证参数
        :param data:
        :return:
        """
        try:
            # 必传参数 version
            if not data["version"] or not data["checkversion"]:
                return JsonResponse(code="999996", msg="缺失必要参数,参数 version,checkversion！")

        except KeyError:
            return JsonResponse(code="999996", msg="参数有误！")

    def post(self, request):
        """
        预测时间 压测结果
        :param request:
        :return:
        """
        data = JSONParser().parse(request)
        result = self.parameter_check(data)
        if result:
            return result

        try:
            type = data["type"]
            if type == 'jz':
                prediction = stress_result.objects.filter(version=data['version'],
                                                          type__in=['predictionJZ', 'lung_prediction'])
                job = stress_result.objects.filter(version=data['version'], type__in=['jobJZ', 'lung_jobJZ'])

                predictionb = stress_result.objects.filter(version=data['checkversion'],
                                                           type__in=['predictionJZ', 'lung_JZ'])
                jobb = stress_result.objects.filter(version=data['checkversion'], type__in=['jobJZ', 'lung_jobJZ'])

                predictionresult = dataCheck(prediction, predictionb)
                jobresult = dataCheck(job, jobb)
                diffresult = dataCheck(job, prediction)
            elif type == 'dy':
                prediction = stress_result.objects.filter(version=data['version'],
                                                          type__in=['predictiondy', 'lung_dy'])
                job = stress_result.objects.filter(version=data['version'], type__in=['jobdy', 'lung_jobdy'])

                predictionb = stress_result.objects.filter(version=data['checkversion'],
                                                           type__in=['predictiondy', 'lung_dy'])
                jobb = stress_result.objects.filter(version=data['checkversion'], type__in=['jobdy', 'lung_jobdy'])

                predictionresult = dataCheck(prediction, predictionb)
                jobresult = dataCheck(job, jobb)
                diffresult = dataCheck(job, prediction)
            else:
                prediction = stress_result.objects.filter(version=data['version'],
                                                          type__in=['prediction', 'lung_prediction'])
                job = stress_result.objects.filter(version=data['version'], type__in=['job', 'lung_job'])

                predictionb = stress_result.objects.filter(version=data['checkversion'],
                                                           type__in=['prediction', 'lung_prediction'])
                jobb = stress_result.objects.filter(version=data['checkversion'], type__in=['job', 'lung_job'])

                predictionresult = dataCheck(prediction, predictionb)
                jobresult = dataCheck(job, jobb)
                diffresult = dataCheck(job, prediction)
            return JsonResponse(data={"predictionresult": predictionresult,
                                      "jobresult": jobresult,
                                      "diffresult": diffresult
                                      }, code="0", msg="成功")

        except Exception as e:
            return JsonResponse(msg="失败", code="999991", exception=e)



class stressResultsave(APIView):
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
            if not data["stressid"]:
                return JsonResponse(code="999996", msg="缺失必要参数,参数 stressid！")

        except KeyError:
            return JsonResponse(code="999996", msg="参数有误！")

    def post(self, request):
        """
        保存压力测试预测性能结果
        预测时间 压测结果
        :param request:
        :return:
        """
        data = JSONParser().parse(request)
        result = self.parameter_check(data)
        if result:
            return result

        try:
            Sf = StressThread(stressid=data['stressid'])
            Sf.SaveResult()
            Sf.SaveRecord()

            return JsonResponse(code="0", msg="成功")
        except Exception as e:
            return JsonResponse(msg="失败", code="999991", exception=e)


# 性能图表
class reportfigure(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def parameter_check(self, data):
        """
        验证参数
        :param data:
        :return:
        """
        try:
            # 必传参数 version
            if not data["type"]:
                return JsonResponse(code="999996", msg="缺失必要参数,参数 type！")

        except KeyError:
            return JsonResponse(code="999996", msg="参数有误！")

    def post(self, request):
        """
        预测时间 压测结果
        :param request:
        :return:
        """
        data = JSONParser().parse(request)
        result = self.parameter_check(data)
        if result:
            return result
        try:
            type = data["type"]
            if type == 'jz':
                predictionData, jobData, lungData, lungjobData = map(stressdataFigure,
                                                                     ["predictionJZ", "jobJZ", "lung_JZ",
                                                                      "lung_jobJZ"])
            elif type == 'dy':
                predictionData, jobData, lungData, lungjobData = map(stressdataFigure,
                                                                     ["predictiondy", "jobdy", "lung_dy",
                                                                      "lung_jobdy"])
            else:
                predictionData, jobData, lungData, lungjobData = map(stressdataFigure,
                                                                     ["prediction", "job", "lung_prediction",
                                                                      "lung_job"])

            return JsonResponse(data={"modlename": predictionData[1],
                                      "lungname": lungData[1],
                                      "predictionFigure": predictionData[0],
                                      "jobFigure": jobData[0],
                                      "lungFigure": lungData[0],
                                      "lungjobFigure": lungjobData[0]
                                      }, code="0", msg="成功")
        except Exception as e:
            return JsonResponse(msg="失败", code="999991", exception=e)