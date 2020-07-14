from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction

from rest_framework.authentication import TokenAuthentication
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView

from TestPlatform.common.api_response import JsonResponse
from TestPlatform.models import stress_record
from TestPlatform.serializers import stressrecord_Deserializer
from ..common.regexUtil import *
from ..common.stress import sequence

logger = logging.getLogger(__name__)  # 这里使用 __name__ 动态搜索定义的 logger 配置，这里有一个层次关系的知识点。


class toolData(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def get(self, request):
        """
        获取压测记录
        :param request:
        :return:
        """
        list = []
        obi = stress_record.objects.get(type=1)
        for i in obi.content.split(","):
            dict = {'key': i, 'value': i}
            list.append(dict)
        return JsonResponse(data={"data": list
                                  }, code="0", msg="成功")


class stresstool(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def parameter_check(self, data):
        """
        验证参数
        :param data:
        :return:
        """
        try:
            # 必传参数 name, version, type
            if not data["loadserver"] or not data["testdata"] or not data["loop_time"]:
                return JsonResponse(code="999996", msg="缺失必要参数！")

        except KeyError:
            return JsonResponse(code="999996", msg="参数有误！")

    def post(self, request):
        """
        执行压测脚本
        :param request:
        :return:
        """
        data = JSONParser().parse(request)
        result = self.parameter_check(data)
        if result:
            return result

        try:
            stressserializer = stressrecord_Deserializer(data=data)
            with transaction.atomic():
                stressserializer.is_valid()
                stressserializer.save()
            stressresult = sequence(data["loadserver"], data["loop_time"], data["testdata"],
                                             data["version"])
            return JsonResponse(data=stressresult, code="0", msg="成功")
        except Exception as e:
            print(e)
            return JsonResponse(msg="失败", code="999991", exception=e)


class Update_base_Data(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def parameter_check(self, data):
        """
        校验参数
        :param data:
        :return:
        """
        try:
            # 校验project_id类型为int
            if not isinstance(data["id"], int):
                return JsonResponse(code="999996", msg="参数有误！")
            # 必传参数 content, status , type
            if not data["content"] or not data["type"] or not data["status"]:
                return JsonResponse(code="999996", msg="参数有误！")

        except KeyError:
            return JsonResponse(code="999996", msg="参数有误！")

    def post(self, request):
        """
        修改基础数据
        :param request:
        :return:
        """
        data = JSONParser().parse(request)
        result = self.parameter_check(data)
        if result:
            return result
        #
        try:
            obj = stress_record.objects.get(id=data["id"])
        except ObjectDoesNotExist:
            return JsonResponse(code="999995", msg="数据不存在！")
        # 查找是否相同名称的项目
        pro_name = stress_record.objects.filter(content=data["content"]).exclude(id=data["id"])
        if len(pro_name):
            return JsonResponse(code="999997", msg="存在相同内容数据")
        else:
            serializer = stressrecord_Deserializer(data=data)
            with transaction.atomic():
                if serializer.is_valid():
                    # 修改数据
                    serializer.update(instance=obj, validated_data=data)
                    return JsonResponse(code="0", msg="成功")
                else:
                    return JsonResponse(code="999998", msg="失败")


class Updatedata(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def parameter_check(self, data):
        """
        验证参数
        :param data:
        :return:
        """
        try:
            # 必传参数 service,type,showid,
            if not data["service"] or not data["showid"] or not data["type"]:
                return JsonResponse(code="999996", msg="必传参数有误！")
            # 环境 类型 online，Autotest
            if data["service"] not in ["staging", "Autotest"]:
                return JsonResponse(code="999996", msg="service参数有误！staging，Autotest")

        except KeyError:
            return JsonResponse(code="999996", msg="参数有误！")
