from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from rest_framework.authentication import TokenAuthentication
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView

from TestPlatform.common.api_response import JsonResponse
from TestPlatform.models import stress_record, stress_data
from TestPlatform.serializers import stressrecord_Deserializer, stress_data_Deserializer
from ..common.regexUtil import *
from ..common.stress import sequence
from ..tools.orthanc.delete_patients import *
from ..tools.duration_verify import *

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


class stressData(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def get(self, request):
        """
        获取项目列表
        :param request:
        :return:
        """
        try:
            page_size = int(request.GET.get("page_size", 20))
            page = int(request.GET.get("page", 1))
        except (TypeError, ValueError):
            return JsonResponse(code="999985", msg="page and page_size must be integer!")
        diseases = request.GET.get("diseases")
        if diseases:
            obi = stress_data.objects.filter(diseases__contains=diseases).order_by("-id")
        else:
            obi = stress_data.objects.all().order_by("-id")
        paginator = Paginator(obi, page_size)  # paginator对象
        total = paginator.num_pages  # 总页数
        try:
            obm = paginator.page(page)
        except PageNotAnInteger:
            obm = paginator.page(1)
        except EmptyPage:
            obm = paginator.page(paginator.num_pages)
        serialize = stress_data_Deserializer(obm, many=True)
        return JsonResponse(data={"data": serialize.data,
                                  "page": page,
                                  "total": total
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
            # 必传参数 loadserver, testdata, loop_time
            if not data["loadserver"] or not data["testdata"] or not data["loop_time"]:
                return JsonResponse(code="999996", msg="缺失必要参数,参数 loadserver, testdata, loop_time！")

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
            testdata=data["testdata"]
            data['testdata']= str(testdata)
            stressserializer = stressrecord_Deserializer(data=data)
            with transaction.atomic():
                stressserializer.is_valid()
                stressserializer.save()
            stressresult = sequence(data["loadserver"], data["loop_time"], testdata,
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


class delete_patients(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def parameter_check(self, data):
        """
        校验参数
        :param data:
        :return:
        """
        try:
            # 必传参数 key, server_ip , type
            if not data["key"] or not data["server_ip"]:
                return JsonResponse(code="999996", msg="参数有误,必传参数 key, server_ip！")

        except KeyError:
            return JsonResponse(code="999996", msg="参数有误！")

    def post(self, request):
        """
        删除数据
        :param request:
        :return:
        """
        data = JSONParser().parse(request)
        result = self.parameter_check(data)
        if result:
            return result
        #
        try:
            delete_patients_duration(data['key'], data['server_ip'])
            return JsonResponse(code="0", msg="成功")
        except ObjectDoesNotExist:
            return JsonResponse(code="999995", msg="数据不存在！")

class duration_verify(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def get(self, request):
        """
        更新持续化记录
        :param request:
        :return:
        """
        data=verify()
        return JsonResponse(data={"data": data
                                  }, code="0", msg="成功")