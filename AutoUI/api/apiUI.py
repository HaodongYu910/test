from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from rest_framework.authentication import TokenAuthentication
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView

from AutoTest.common.api_response import JsonResponse
from ..serializers import autoui_Serializer, autoui_Deserializer
from AutoDicom.common.deletepatients import *
from AutoDicom.common.dicomBase import baseTransform
from AutoUI.common.autouitest import *

logger = logging.getLogger(__name__)  # 这里使用 __name__ 动态搜索定义的 logger 配置


class getAutoUI(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def get(self, request):
        """
        获取autoui数据
        :param request:
        :return:
        """
        try:
            page_size = int(request.GET.get("page_size", 20))
            page = int(request.GET.get("page", 1))
            version = request.GET.get("version")
            type = request.GET.get("type")
        except (TypeError, ValueError):
            return JsonResponse(code="999985", msg="page and page_size must be integer!")

        if version:
            obi = autoui.objects.filter(version=version, type=type).order_by("version")
        elif type:
            obi = autoui.objects.filter(type=type).order_by("version")
        else:
            obi = autoui.objects.all().order_by("-autoid")
        paginator = Paginator(obi, page_size)  # paginator对象
        total = paginator.num_pages  # 总页数
        try:
            obm = paginator.page(page)
        except PageNotAnInteger:
            obm = paginator.page(1)
        except EmptyPage:
            obm = paginator.page(paginator.num_pages)
        serialize = autoui_Serializer(obm, many=True)
        for i in serialize.data:
            try:
                i["setup"] = baseTransform(i["setup"], 'case')
                i["cases"] = baseTransform(i["cases"], 'case')
                i["tearDown"] = baseTransform(i["tearDown"], 'case')
                # count = auto_uirecord.objects.filter(smokeid=i['id']).aggregate(result_nums=Count("result"))
                # success = auto_uirecord.objects.filter(smokeid=i['id'], result='匹配成功').aggregate(result_nums=Count("result"))
                # fail = auto_uirecord.objects.filter(smokeid=i['id'], result='匹配失败').aggregate(result_nums=Count("result"))
                i["progress"] = '%.2f' % (int(i["progress"]) * 100)
                # i["success"] = success["result_nums"]
                # i["fail"] = fail['result_nums']
                # i["aifail"] = int(count['result_nums']) - int(success["result_nums"]) - int(fail['result_nums'])
                hostobj = Server.objects.get(id=i["hostid"])
                i["hostid"] = hostobj.host
            except Exception as e:
                i["host"] = "Null"
                continue
        return JsonResponse(data={"data": serialize.data,
                                  "page": page,
                                  "total": total
                                  }, code="0", msg="成功")


class AddAutoUI(APIView):
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
            if not data["hostid"] or not data["version"]:
                return JsonResponse(code="999996", msg="参数有误！")

        except KeyError:
            return JsonResponse(code="999996", msg="参数有误！")

    def post(self, request):
        """
        新增自动测试
        :param request:
        :return:
        """
        data = JSONParser().parse(request)
        result = self.parameter_check(data)
        if result:
            return result
        try:
            data["setup"] = str(data["setup"])[1:-1] if data["setup"] != [] else None
            data["cases"] = str(data["cases"])[1:-1]
            data["tearDown"] = str(data["tearDown"])[1:-1] if data["setup"] != [] else None
            autoadd = autoui_Serializer(data=data)
            with transaction.atomic():
                autoadd.is_valid()
                autoadd.save()

            return JsonResponse(code="0", msg="成功")
        except Exception as e:
            return JsonResponse(code="999995", msg="{0}".format(e))


class UpdateAutoUI(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def parameter_check(self, data):
        """
        校验参数
        :param data:
        :return:
        """
        try:
            # 校验id类型为int
            if not isinstance(data["autoid"], int):
                return JsonResponse(code="999996", msg="参数有误！")
            # 必传参数 id,version
            if not data["autoid"] or not data["version"]:
                return JsonResponse(code="999996", msg="参数有误 必传参数 id, version！")

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
        data["setup"] = str(data["setup"])[1:-1]
        # data["cases"] = str(data["cases"])[1:-1]
        data["tearDown"] = str(data["tearDown"])[1:-1]
        try:
            autoobj = autoui.objects.get(id=data["autoid"])
        except Exception as e:
            return JsonResponse(code="999995", msg="数据不存在！")
        # 查找是否相同名称
        name = autoui.objects.filter(version=data["version"]).exclude(id=data["autoid"])
        if len(name):
            return JsonResponse(code="999997", msg="存在相同内容数据")
        else:
            serializer = autoui_Deserializer(data=data)
            with transaction.atomic():
                if serializer.is_valid():
                    # 修改数据
                    serializer.update(instance=autoobj, validated_data=data)
                    return JsonResponse(code="0", msg="成功")
                else:
                    return JsonResponse(code="999998", msg="失败")


class DelAutoUI(APIView):
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
            if not isinstance(data["ids"], list):
                return JsonResponse(code="999996", msg="参数有误！")
            for i in data["ids"]:
                if not isinstance(i, int):
                    return JsonResponse(code="999996", msg="参数有误！")
        except KeyError:
            return JsonResponse(code="999996", msg="参数有误！")

    def post(self, request):
        """
        删除信息
        :param request:
        :return:
        """
        data = JSONParser().parse(request)
        result = self.parameter_check(data)
        if result:
            return result
        try:
            for j in data["ids"]:
                try:
                    obj = autoui.objects.filter(autoid=j)
                    obj.delete()
                except Exception as e:
                    logger.error("删除smoke数据失败")
            return JsonResponse(code="0", msg="成功")
        except ObjectDoesNotExist:
            return JsonResponse(code="999995", msg="项目不存在！")


class DisableAutoUI(APIView):
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
            if not isinstance(data["autoid"], int):
                return JsonResponse(code="999996", msg="参数有误！")
        except KeyError:
            return JsonResponse(code="999996", msg="参数有误！")

    def post(self, request):
        """
        禁用项目
        :param request:
        :return:
        """
        data = JSONParser().parse(request)
        result = self.parameter_check(data)
        if result:
            return result
        # 查找是否存在
        try:
            auto = AutoUiThread(autoid=data["autoid"])
            auto.UiStop()
            return JsonResponse(code="0", msg="成功")
        except ObjectDoesNotExist:
            return JsonResponse(code="999995", msg="数据不存在！")


class EnableAutoUI(APIView):
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
            if not isinstance(data["autoid"], int):
                return JsonResponse(code="999996", msg="参数有误！")
        except KeyError:
            return JsonResponse(code="999996", msg="参数有误！")

    def post(self, request):
        """
        启用项目
        :param request:
        :return:
        """
        data = JSONParser().parse(request)
        result = self.parameter_check(data)
        if result:
            return result
        # 查找项目是否存在
        try:
            # 执行测试
            try:
                auto = AutoUiThread(autoid=data["autoid"])
                obj = auto_uirecord.objects.filter(autoid=data["autoid"])
                obj.delete()
                auto.addUitest()
                auto.Uitest()
            except Exception as e:
                logger.error(e)
                return JsonResponse(msg="执行失败", code="999991", exception=e)
            return JsonResponse(code="0", msg="成功")
        except ObjectDoesNotExist:
            return JsonResponse(code="999995", msg="数据不存在！")
