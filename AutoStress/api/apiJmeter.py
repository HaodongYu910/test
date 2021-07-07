from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db import transaction

from rest_framework.authentication import TokenAuthentication
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView

from AutoProject.common.api_response import JsonResponse
from ..serializers import stress_Deserializer, stress_jmeter_Serializer, stress_jmeter_Deserializer

from AutoDicom.common.dicomBase import baseTransform
from AutoDicom.common.deletepatients import *
from ..common.hybrid import HybridThread
from ..common.single import SingleThread
from ..common.manual import ManualThread
from ..common.stressTest import StressThread
from ..common.jmeter import JmeterThread
from ..common.StrategyDetail import strategyList

from AutoProject.models import uploadfile, project_version
from AutoProject.serializers import uploadfile_Deserializer
from ..models import stress, stress_record, stress_jmeter
import os
import shutil
import datetime


logger = logging.getLogger(__name__)  # 这里使用 __name__ 动态搜索定义的 logger 配置


# 获取 jmeter 列表
class jmeterList(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def get(self, request):
        """
        获取性能列表数据
        :param request:
        :return:
        """
        try:
            page_size = int(request.GET.get("page_size", 999))
            page = int(request.GET.get("page", 1))
            project_id = int(request.GET.get("project_id", 1))
        except (TypeError, ValueError):
            return JsonResponse(code="999985", msg="page and page_size must be integer!")
        version = request.GET.get("version")

        # 判断查询数据类型
        if version:
            obi = stress_jmeter.objects.filter(status=True, project_id=project_id).order_by("-stressid")
        else:
            obi = stress.objects.filter(project_id=project_id).order_by("-stressid")
        paginator = Paginator(obi, page_size)  # paginator对象
        total = paginator.num_pages  # 总页数
        count = paginator.count  # 总页数
        try:
            obm = paginator.page(page)
        except PageNotAnInteger:
            obm = paginator.page(1)
        except EmptyPage:
            obm = paginator.page(paginator.num_pages)
        serialize = stress_Deserializer(obm, many=True)
        for i in serialize.data:
            try:
                i["version"] = project_version.objects.get(id=i["version"]).version
            except:
                continue
            i["testdata"] = baseTransform(i["testdata"], 'dictionary')
            i["type"] = False
        return JsonResponse(data={"data": serialize.data,
                                  "page": page,
                                  "total": total,
                                  "count": count
                                  }, code="0", msg="成功")

class jmeterDetail(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def get(self, request):
        """
                获取jmeter详情
                :param request:
                :return:
                """
        try:
            stressid = request.GET.get("stressid")
            obj = stress.objects.filter(stressid=stressid)
            stressserializer = stress_Deserializer(obj, many=True)

            for i in stressserializer.data:
                try:
                    i["version"] = project_version.objects.get(id=i["version"]).version
                except:
                    logger.error("version")

            return JsonResponse(data={"data": stressserializer.data
                                      }, code="0", msg="成功")
        except Exception as e:
            logger.error(e)
            return JsonResponse(msg="失败", code="999991", exception=e)



class addJmeter(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def parameter_check(self, data):
        """
        校验参数
        :param data:
        :return:
        """
        try:
            # 必传参数 stressID  uploadID
            if not data["stressID"] or not data["uploadID"]:
                return JsonResponse(code="999996", msg="参数有误,必传参数 uploadID, stressID！")

        except KeyError:
            return JsonResponse(code="999996", msg="参数有误,必传参数uploadID, stressID！！")

    def post(self, request):
        """
        添加jmeter 信息
        :param request:
        :return:
        """
        data = JSONParser().parse(request)
        result = self.parameter_check(data)
        if result:
            return result
        try:
            uploadObj = uploadfile.objects.get(id=data['uploadID'])
            data["route"] = uploadObj.fileurl

            Stressadd = stress_jmeter_Serializer(data=data)
            with transaction.atomic():
                Stressadd.is_valid()
                strdata = Stressadd.save()
            return JsonResponse(code="0", msg="成功")
        except Exception as e:
            return JsonResponse(code="999995", msg="{0}".format(e))


# 修改压测信息
class updateJmeter(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def parameter_check(self, data):
        """
        校验参数
        :param data:
        :return:
        """
        try:
            # 必传参数 id
            if not data["id"]:
                return JsonResponse(code="999996", msg="参数有误,必传参数 id！")

        except KeyError:
            return JsonResponse(code="999996", msg="参数有误！")

    def post(self, request):
        """
        修改jmeter 配置
        :param request:
        :return:
        """
        data = JSONParser().parse(request)
        result = self.parameter_check(data)
        if result:
            return result
        try:

            obj = stress_jmeter.objects.get(id=data["id"])
            serializer = stress_Deserializer(data=data)
            with transaction.atomic():
                if serializer.is_valid():
                    # 修改数据
                    serializer.update(instance=obj, validated_data=data)
            return JsonResponse(code="0", msg="成功")
        except ObjectDoesNotExist:
            return JsonResponse(code="999995", msg="数据不存在！")


class delJmeter(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def parameter_check(self, data):
        """
        校验参数
        :param data:
        :return:
        """
        try:
            # 校验id
            if not data["id"]:
                return JsonResponse(code="999996", msg="参数有误！")
        except KeyError:
            return JsonResponse(code="999996", msg="参数有误！")

    def post(self, request):
        """
        删除性能测试
        :param request:
        :return:
        """
        data = JSONParser().parse(request)
        result = self.parameter_check(data)
        if result:
            return result
        try:
            obj = stress_jmeter.objects.get(id=data["id"])
            obj.status =False
            obj.save()
            return JsonResponse(code="0", msg="成功")
        except ObjectDoesNotExist:
            return JsonResponse(code="999995", msg="数据不存在！")



