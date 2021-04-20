from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.conf import settings
from django.db import transaction

from rest_framework.authentication import TokenAuthentication
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView

from AutoProject.common.api_response import JsonResponse
from AutoProject.serializers import install_Deserializer
import logging
from AutoProject.common.InstallSmoke import InGoldThread

import os
logger = logging.getLogger(__name__)  # 这里使用 __name__ 动态搜索定义的 logger 配置

class Smoketest(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def get(self, request):
        """
        冒烟测试
        :param request:
        :return:
        user
        """

        version = request.GET.get("version")

        try:
            if version is None or version == "":
                return JsonResponse(code="999998", msg="参数错误（必传参数：version 可选参数：serverIP）")
            else:
                testThread = InGoldThread(version=version)
                # 设为保护线程，主进程结束会关闭线程
                testThread.setDaemon(True)
                # 开始线程
                testThread.start()
                return JsonResponse(code="0", msg="Success")

        except ObjectDoesNotExist:
            return JsonResponse(code="999998", msg="错误")