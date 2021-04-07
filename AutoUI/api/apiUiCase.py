from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from rest_framework.authentication import TokenAuthentication
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView

from AutoTest.common.api_response import JsonResponse
from ..serializers import autoui_Deserializer,autocase_Serializer
from AutoDicom.common.deletepatients import *
from AutoTest.models import uploadfile
from AutoDicom.common.dicomBase import baseTransform
from AutoUI.common.autouitest import *
from  django.db import transaction

logger = logging.getLogger(__name__)  # 这里使用 __name__ 动态搜索定义的 logger 配置

class getUICase(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def get(self, request):
        """
        获取用例
        :param request:
        :return:
        """
        try:
            page_size = int(request.GET.get("page_size", 20))
            page = int(request.GET.get("page", 1))
            type = request.GET.get("type")
            name = request.GET.get("name")
        except (TypeError, ValueError):
            return JsonResponse(code="999985", msg="page and page_size must be integer!")
        if name:
            obi = auto_uicase.objects.filter(name=name).order_by("id")
        elif type:
            obi = auto_uicase.objects.filter(type=type).order_by("id")
        else:
            obi = auto_uicase.objects.all().order_by("-id")
        paginator = Paginator(obi, page_size)  # paginator对象
        total = paginator.num_pages  # 总页数
        try:
            obm = paginator.page(page)
        except PageNotAnInteger:
            obm = paginator.page(1)
        except EmptyPage:
            obm = paginator.page(paginator.num_pages)
        serialize = autocase_Serializer(obm, many=True)

        for i in serialize.data:
            try:
                i["testdata"]= baseTransform(i["testdata"],'base')
            except:
                continue
        return JsonResponse(data={"data": serialize.data,
                                  "page": page,
                                  "total": total
                                  }, code="0", msg="成功")

class AddUICase(APIView):
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
            if not data["type"] or not data["name"]:
                return JsonResponse(code="999996", msg="参数有误！")

        except KeyError:
            return JsonResponse(code="999996", msg="参数有误！")

    def post(self, request):
        """
        新增用例
        :param request:
        :return:
        """
        data = JSONParser().parse(request)
        result = self.parameter_check(data)
        if result:
            return result
        try:
            # data["testdata"] = str(data["testdata"])[1:-1]
            dict = data['filedict']
            autoadd = autocase_Serializer(data=data)
            # 查找是否相同名称
            name = auto_uicase.objects.filter(name=data["name"])
            if len(name):
                return JsonResponse(code="999997", msg="存在相同用例名")
            else:
                with transaction.atomic():
                    autoadd.is_valid()
                    acase = autoadd.save()
                if dict != {}:
                    for k, v in dict.items():
                        try:
                            obj = uploadfile.objects.get(id=v)
                            obj.fileid = str(acase.caseid)
                            obj.save()
                        except Exception as e:
                            logger.error("更新upload数据失败{0},错误：{1}".format(v, e))
                            continue
                return JsonResponse(code="0", msg="成功")
        except Exception as e:
            return JsonResponse(code="999995", msg="{0}".format(e))

class UpdateUICase(APIView):
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
            # 必传参数 content, predictor , type
            if not data["caseid"] or not data["name"]or not data["type"]:
                return JsonResponse(code="999996", msg="参数有误 必传参数 name, caseid , type！")
        except KeyError:
            return JsonResponse(code="999996", msg="参数有误 必传参数 name, id , type！！")

    def post(self, request):
        """
        修改用例
        :param request:
        :return:
        """
        data = JSONParser().parse(request)
        result = self.parameter_check(data)
        dict = data['filedict']
        if result:
            return result
        #
        try:
            autoobj = auto_uicase.objects.get(id=data["id"])
        except Exception as e:
            return JsonResponse(code="999995", msg="数据不存在！")
        # 查找是否相同名称
        name = auto_uicase.objects.filter(name=data["name"]).exclude(id=data["caseid"])
        if len(name):
            return JsonResponse(code="999997", msg="存在相同用例名")
        else:
            serializer = autoui_Deserializer(data=data)
            with transaction.atomic():
                if serializer.is_valid():
                    # 修改数据
                    serializer.update(instance=autoobj, validated_data=data)
                    if dict != {}:
                        for k, v in dict.items():
                            try:
                                obj = uploadfile.objects.get(id=v)
                                obj.fileid = str(data["id"])
                                obj.save()
                            except Exception as e:
                                logger.error("更新upload数据失败{0},错误：{1}".format(v, e))
                                continue
                    return JsonResponse(code="0", msg="成功")
                else:
                    return JsonResponse(code="999998", msg="失败")


class DelUICase(APIView):
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
                    obj = auto_uicase.objects.filter(id=j)
                    obj.delete()
                except Exception as e:
                    logger.error("删除smoke数据失败")
            return JsonResponse(code="0", msg="成功")
        except ObjectDoesNotExist:
            return JsonResponse(code="999995", msg="项目不存在！")


class DisableUICase(APIView):
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
            obj = auto_uicase.objects.get(caseid=data["id"])
            obj.status = False
            obj.save()
            return JsonResponse(code="0", msg="成功")
        except ObjectDoesNotExist:
            return JsonResponse(code="999995", msg="项目不存在！")


class EnableUICase(APIView):
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
            obj = auto_uicase.objects.get(caseid=data["id"])
            obj.status = True
            obj.save()

            return JsonResponse(code="0", msg="成功")
        except ObjectDoesNotExist:
            return JsonResponse(code="999995", msg="数据不存在！")

