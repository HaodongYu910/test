from rest_framework.authentication import TokenAuthentication
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
import logging
from AutoProject.common.api_response import JsonResponse
from ..common.saveResult import *
from ..common.PerformanceResult import *
from ..common.stressfigure import stressdataFigure
from AutoProject.models import dictionary
from  ..common.saveResult import ResultThread

logger = logging.getLogger(__name__)  # 这里使用 __name__ 动态搜索定义的 logger 配置


class StressModel(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def get(self, request):
        """
        获取性能测试版本模型
        :param request:
        :return:
        """
        options = []
        optionsdict = {}

        obj = dictionary.objects.filter(type="model", status=True)
        for i in obj:
            if optionsdict.__contains__(i.remarks) is False:
                optionsdict[i.remarks] = [{"value": i.id,
                                 "label": i.value}]
            else:
                optionsdict[i.remarks].append({"value": i.id,
                                           "label": i.value})

        for k, v in optionsdict.items():
            children = {
                "value": k,
                "label": k,
                "children": v}
            options.append(children)
        return JsonResponse(data={"data": options
                                  }, code="0", msg="成功")



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
            result = ResultThread(stressid=data['stressid'])
            result.setDaemon(True)
            result.start()

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
            if data["type"] == 'jz':
                type = ['predictionJZ', 'jobJZ']
            elif data["type"] == 'dy':
                type = ['predictiondy', 'jobdy']
            else:
                type = ['prediction', 'job']

            chartData = stressdataFigure(data['diseases'], type)

            return JsonResponse(data={"chartData": chartData
                                      }, code="0", msg="成功")
        except Exception as e:
            return JsonResponse(msg="失败", code="999991", exception=e)
