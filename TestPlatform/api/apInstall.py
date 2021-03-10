from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from rest_framework.authentication import TokenAuthentication
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from django.db import transaction
from TestPlatform.common.api_response import JsonResponse
from TestPlatform.serializers import install_Deserializer
from TestPlatform.common.install import InstallThread
from Dicom.common.deletepatients import *
from ..models import install
from Dicom.common.dicomBase import baseTransform

logger = logging.getLogger(__name__)  # 这里使用 __name__ 动态搜索定义的 logger 配置


class getInstall(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def get(self, request):
        """
        获取Install数据
        :param request:
        :return:
        """
        try:
            page_size = int(request.GET.get("page_size", 20))
            page = int(request.GET.get("page", 1))
        except (TypeError, ValueError):
            return JsonResponse(code="999985", msg="page and page_size must be integer!")
        version = request.GET.get("version")

        if version:
            obi = install.objects.filter(version=version).order_by("version")
        else:
            obi = install.objects.all().order_by("-id")
        paginator = Paginator(obi, page_size)  # paginator对象
        total = paginator.num_pages  # 总页数
        try:
            obm = paginator.page(page)
        except PageNotAnInteger:
            obm = paginator.page(1)
        except EmptyPage:
            obm = paginator.page(paginator.num_pages)
        serialize = install_Deserializer(obm, many=True)

        return JsonResponse(data={"data": serialize.data,
                                  "page": page,
                                  "total": total
                                  }, code="0", msg="成功")


class AddInstall(APIView):
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
        新增基础数据
        :param request:
        :return:
        """
        data = JSONParser().parse(request)
        result = self.parameter_check(data)
        if result:
            return result
        try:
            Installadd = install_Deserializer(data=data)

            with transaction.atomic():
                Installadd.is_valid()
                Installadd.save()
            return JsonResponse(code="0", msg="成功")
        except Exception as e:
            return JsonResponse(code="999995", msg="{0}".format(e))


class UpdateInstall(APIView):
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
            if not isinstance(data["hostid"], int):
                return JsonResponse(code="999996", msg="参数有误！")
            # 必传参数 content, predictor , type
            if not data["id"] or not data["version"]:
                return JsonResponse(code="999996", msg="参数有误 必传参数 content, predictor , type！")

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
        try:
            Installobj = install.objects.get(id=data["id"])
        except Exception as e:
            return JsonResponse(code="999995", msg="数据不存在！")

        serializer = install_Deserializer(data=data)
        with transaction.atomic():
            if serializer.is_valid():
                # 修改数据
                serializer.update(instance=Installobj, validated_data=data)
                return JsonResponse(code="0", msg="成功")
            else:
                return JsonResponse(code="999998", msg="失败")


class DelInstall(APIView):
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
                    obj = install.objects.filter(id=j)
                    obj.delete()
                except Exception as e:
                    logger.error("删除Install数据失败")
            return JsonResponse(code="0", msg="成功")
        except ObjectDoesNotExist:
            return JsonResponse(code="999995", msg="项目不存在！")


class DisableInstall(APIView):
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
            obj = install.objects.get(id=data["id"])
            testThread = InstallThread(data["id"])
            # 设为保护线程，主进程结束会关闭线程
            testThread.setFlag = False
            obj.status = False
            obj.save()
            return JsonResponse(code="0", msg="成功")
        except ObjectDoesNotExist:
            return JsonResponse(code="999995", msg="项目不存在！")


class EnableInstall(APIView):
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
            obj = install.objects.get(id=data["id"])

            testThread = InstallThread(id=data["id"])
            testThread.setDaemon(True)
            # 开始线程
            testThread.start()
            # # 下载版本
            # localpath,version = testThread.download()
            # 安装版本
            testThread.install()
            # 重启系统
            testThread.restart()
            # 执行 金标准测试
            testThread.goldsmoke()
            # 执行 UI测试
            testThread.UiTest()
            # 变更状态
            # obj.status = False
            # obj.type = 1
            # obj.save()

            return JsonResponse(code="0", msg="成功")
        except ObjectDoesNotExist:
            return JsonResponse(code="999995", msg="项目不存在！")
