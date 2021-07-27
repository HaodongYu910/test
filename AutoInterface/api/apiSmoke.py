from django.core.exceptions import ObjectDoesNotExist

from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView

from AutoProject.common.api_response import JsonResponse
import logging
from AutoProject.common.biomind import smoke

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
                smoke(version=version)
                return JsonResponse(code="0", msg="Success")

        except ObjectDoesNotExist:
            return JsonResponse(code="999998", msg="错误")