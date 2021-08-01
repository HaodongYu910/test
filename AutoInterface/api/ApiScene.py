import logging

import time
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db import transaction
from django.db.models import Q
from django.http import StreamingHttpResponse
from rest_framework.authentication import TokenAuthentication
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.utils import json
from rest_framework.views import APIView

from AutoProject.common.WriteDocx import Write
from AutoProject.common.api_response import JsonResponse
from AutoProject.common.common import record_dynamic, check_json
from AutoInterface.common.loadSwaggerApi import swagger_api
from AutoProject.models import Project
from AutoInterface.models import AutomationTestCase, AutomationCaseApi
from AutoInterface.serializers import AutomationCaseApiSerializer, AutomationTestCaseSerializer

logger = logging.getLogger(__name__)  # 这里使用 __name__ 动态搜索定义的 logger 配置，这里有一个层次关系的知识点。


class ApiSceneDetail(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def get(self, request):
        """
        获取接口列表
        :param request:
        :return:
        """
        try:
            case_id = int(request.GET.get("case_id"))
        except (TypeError, ValueError):
            return JsonResponse(code="999985", msg="case_id must be integer!")

        try:
            obj = AutomationTestCase.objects.filter(id=case_id)
            CaseSerialize = AutomationTestCaseSerializer(obj, many=True)
        except ObjectDoesNotExist:
            return JsonResponse(code="999995", msg="用例不存在!")

        try:
            stepObj = AutomationCaseApi.objects.filter(automationTestCase_id=case_id)
            serialize = AutomationCaseApiSerializer(stepObj, many=True)
        except PageNotAnInteger:
            return JsonResponse(code="999993", msg="序列化取数据错误!")

        return JsonResponse(data={
            "CaseInfo": CaseSerialize.data,
            "StepInfo": serialize.data
            }, code="0", msg="成功!")

