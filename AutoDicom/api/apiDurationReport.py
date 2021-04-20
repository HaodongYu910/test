from rest_framework.authentication import TokenAuthentication
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView

from AutoProject.common.api_response import JsonResponse
import logging
from ..common.DurarionReport import ReportThread
from AutoProject.scheduletask import DurationTask


logger = logging.getLogger(__name__)  # 这里使用 __name__ 动态搜索定义的 logger 配置


class DurationReport(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def get(self, request):
        """
        持续化数据报告
        :param request:
        :return:
        """
        try:
            duration_id = request.GET.get("id")
            diseases = request.GET.get("diseases")
            # DurationTask()
        except (TypeError, ValueError):
            return JsonResponse(code="999985", msg="duration_id 必传字段!")
        try:
            testThread = ReportThread(id=duration_id,diseases=diseases)
            data = testThread.report()
            return JsonResponse(data={"data": data,
                                      }, code="0", msg="成功")
        except Exception as e:
           return JsonResponse(code="999986", msg="报告生成失败")

