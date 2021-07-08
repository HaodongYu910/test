from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db import transaction

from rest_framework.authentication import TokenAuthentication
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView

from AutoProject.common.api_response import JsonResponse
import logging

from ..common.Monitor import monitor


logger = logging.getLogger(__name__)  # 这里使用 __name__ 动态搜索定义的 logger 配置


class getMonitor(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def get(self, request):
        """
        重启服务监控 或新增
        :param request:
        :return:
        """
        try:
            operation = request.GET.get("operation", "restart")
            host_id = int(request.GET.get("host_id", 1))
            monitor(operation=operation, host_id=host_id)
        except (TypeError, ValueError):
            return JsonResponse(code="999985", msg="page and page_size must be integer!")

        return JsonResponse(code="0", msg="成功")
