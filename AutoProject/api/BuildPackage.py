import logging

from crontab import CronTab
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from rest_framework.authentication import TokenAuthentication
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView

from AutoProject.common.api_response import JsonResponse
from AutoProject.common.common import record_dynamic
from AutoProject.models import build_package, build_package_detail, Server, Token
from AutoProject.serializers import build_packageSerializer, build_packageDeserializer

logger = logging.getLogger(__name__)  # 这里使用 __name__ 动态搜索定义的 logger 配置，这里有一个层次关系的知识点。


class BuildList(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def get(self, request):
        """
        获取列表
        :param request:
        :return:
        """
        try:
            page_size = int(request.GET.get("page_size", 20))
            page = int(request.GET.get("page", 1))
        except (TypeError, ValueError):
            return JsonResponse(code="999985", msg="page and page_size must be integer!")
        name = request.GET.get("name")
        if name:
            obi = build_package.objects.filter(name__contains=name).order_by("-id")
        else:
            obi = build_package.objects.all().order_by("-id")
        paginator = Paginator(obi, page_size)  # paginator对象
        total = paginator.num_pages  # 总页数
        try:
            obm = paginator.page(page)
        except PageNotAnInteger:
            obm = paginator.page(1)
        except EmptyPage:
            obm = paginator.page(paginator.num_pages)
        serialize = build_packageSerializer(obm, many=True)
        for i in serialize.data:
            if i["Host"] is not None:
                i["Host"] = Server.objects.get(id=i["Host"]).host

        return JsonResponse(data={"data": serialize.data,
                                  "page": page,
                                  "total": total
                                  }, code="0", msg="成功")


class AddBuild(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def parameter_check(self, data):
        """
        验证参数
        :param data:
        :return:
        """
        try:
            # 必传参数 name, service
            if not data["name"] or not data["service"]:
                return JsonResponse(code="999996", msg="参数有误！")

        except KeyError:
            return JsonResponse(code="999996", msg="参数有误！")

    def post(self, request):
        """
        新增 build
        :param request:
        :return:
        """
        data = JSONParser().parse(request)
        result = self.parameter_check(data)
        if result:
            return result
        data["user"] = Token.objects.get(key=data["user"]).user_id
        build_package_serializer = build_packageDeserializer(data=data)

        try:
            build_package.objects.get(name=data["name"])
            return JsonResponse(code="999997", msg="存在相同名称")
        except ObjectDoesNotExist:
            with transaction.atomic():
                if build_package_serializer.is_valid():
                    # 保持新项目
                    build_package_serializer.save()
                    return JsonResponse(data={
                            "build_package_id": build_package_serializer.data.get("id")
                        }, code="0", msg="成功")
                else:
                    return JsonResponse(code="999998", msg=build_package_serializer.errors)


class UpdateBuild(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def parameter_check(self, data):
        """
        校验参数
        :param data:
        :return:
        """
        try:
            # 校验package_id类型为int
            if not isinstance(data["package_id"], int):
                return JsonResponse(code="999996", msg="参数有误！")
            # 必传参数 service
            if not data["service"] or not data["code"] or not data["type"]:
                return JsonResponse(code="999996", msg="参数有误！")
        except KeyError:
            return JsonResponse(code="999996", msg="参数有误！")

    def post(self, request):
        """
        修改项目
        :param request:
        :return:
        """
        data = JSONParser().parse(request)
        result = self.parameter_check(data)
        if result:
            return result
        # 查找项目是否存在
        try:
            obj = build_package.objects.get(id=data["package_id"])
            if not request.user.is_superuser and obj.user.is_superuser:
                return JsonResponse(code="999983", msg="无操作权限！")
        except ObjectDoesNotExist:
            return JsonResponse(code="999995", msg="数据不存在！")
        # 查找是否相同名称的项目
        build_name = build_package.objects.filter(name=data["name"]).exclude(id=data["package_id"])
        if len(build_name):
            return JsonResponse(code="999997", msg="存在相同构建名称")
        else:
            serializer = build_packageDeserializer(data=data)
            with transaction.atomic():
                if serializer.is_valid():
                    # 修改项目
                    serializer.update(instance=obj, validated_data=data)
                    return JsonResponse(code="0", msg="成功")
                else:
                    return JsonResponse(code="999998", msg="失败")


class DelBuild(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def parameter_check(self, data):
        """
        校验参数
        :param data:
        :return:
        """
        try:
            # 校验build_package_id类型为int
            if not isinstance(data["ids"], list):
                return JsonResponse(code="999996", msg="参数有误！")
            for i in data["ids"]:
                if not isinstance(i, int):
                    return JsonResponse(code="999996", msg="参数有误！")
        except KeyError:
            return JsonResponse(code="999996", msg="参数有误！")

    def post(self, request):
        """
        删除项目
        :param request:
        :return:
        """
        data = JSONParser().parse(request)
        result = self.parameter_check(data)
        if result:
            return result
        try:
            for i in data["ids"]:
                try:
                    obj = build_package.objects.get(id=i)
                    if not request.user.is_superuser and obj.user.is_superuser:
                        return JsonResponse(code="999983", msg=str(obj)+"无操作权限！")
                except ObjectDoesNotExist:
                    return JsonResponse(code="999995", msg="项目不存在！")
            for j in data["ids"]:
                obj = build_package.objects.filter(id=j)
                obj.delete()
                # my_user_cron = CronTab(user=True)
                # my_user_cron.remove_all(comment=j)
                # my_user_cron.write()
            return JsonResponse(code="0", msg="成功")
        except ObjectDoesNotExist:
            return JsonResponse(code="999995", msg="项目不存在！")


class DisableBuild(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def parameter_check(self, data):
        """
        校验参数
        :param data:
        :return:
        """
        try:
            # 校验build_package_id类型为int
            if not isinstance(data["build_package_id"], int):
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
        # 查找项目是否存在
        try:
            obj = build_package.objects.get(id=data["build_package_id"])
            if not request.user.is_superuser and obj.user.is_superuser:
                return JsonResponse(code="999983", msg=str(obj) + "无操作权限！")
            obj.status = False
            obj.save()
            record_dynamic(build_package=data["build_package_id"],
                           _type="禁用", operationObject="项目", user=request.user.pk, data=obj.name)
            return JsonResponse(code="0", msg="成功")
        except ObjectDoesNotExist:
            return JsonResponse(code="999995", msg="项目不存在！")


class EnableBuild(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def parameter_check(self, data):
        """
        校验参数
        :param data:
        :return:
        """
        try:
            # 校验build_package_id类型为int
            if not isinstance(data["build_package_id"], int):
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
            obj = build_package.objects.get(id=data["build_package_id"])
            if not request.user.is_superuser and obj.user.is_superuser:
                return JsonResponse(code="999983", msg=str(obj) + "无操作权限！")
            obj.status = True
            obj.save()
            record_dynamic(build_package=data["build_package_id"],
                           _type="禁用", operationObject="项目", user=request.user.pk, data=obj.name)
            return JsonResponse(code="0", msg="成功")
        except ObjectDoesNotExist:
            return JsonResponse(code="999995", msg="项目不存在！")


