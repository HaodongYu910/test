import logging

from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db import transaction
from rest_framework.authentication import TokenAuthentication
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView

from AutoTest.common.api_response import JsonResponse
from AutoTest.common.common import record_dynamic
from AutoTest.models import Project, Server
from AutoTest.serializers import ServerSerializer, ProjectSerializer

logger = logging.getLogger(__name__)  # 这里使用 __name__ 动态搜索定义的 logger 配置，这里有一个层次关系的知识点。


class HostTotal(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def get(self, request):
        """
        获取host列表
        :param request:
        :return:
        """
        try:
            page_size = int(request.GET.get("page_size", 20))
            page = int(request.GET.get("page", 1))
            name = request.GET.get("name")
        except (TypeError, ValueError):
            return JsonResponse(code="999995", msg="page and page_size must be integer！")
        if request.GET.get("project_id") is True:
            project_id = request.GET.get("project_id")
            if not project_id.isdecimal():
                return JsonResponse(code="999995", msg="参数有误！")
            try:
                pro_data = Project.objects.get(id=project_id)
            except ObjectDoesNotExist:
                return JsonResponse(code="999995", msg="项目不存在！")
            pro_data = ProjectSerializer(pro_data)
            if not pro_data.data["status"]:
                return JsonResponse(code="999985", msg="该项目已禁用")
            if name:
                obi = Server.objects.filter(name__contains=name, project=project_id).order_by("id")
            else:
                obi = Server.objects.filter(project=project_id).order_by("id")
        else:
            if name:
                obi = Server.objects.filter(name__contains=name).order_by("id")
            else:
                obi = Server.objects.filter().order_by("id")
            paginator = Paginator(obi, page_size)  # paginator对象
            total = paginator.num_pages  # 总页数
        try:
            obm = paginator.page(page)
        except PageNotAnInteger:
            obm = paginator.page(1)
        except EmptyPage:
            obm = paginator.page(paginator.num_pages)
        serialize = ServerSerializer(obm, many=True)
        for i in serialize.data:
            if i["protocol"] == 'https':
                i["protocol"] = False
            else:
                i["protocol"] = True
        return JsonResponse(data={"data": serialize.data,
                                  "page": page,
                                  "total": total
                                  }, code="0", msg="成功！")


class AddHost(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def parameter_check(self, data):
        """
        校验参数
        :param data:
        :return:
        """
        try:
            # 必传参数 name, host
            if not data["name"] or not data["host"]:
                return JsonResponse(code="999995", msg="参数有误！")
        except KeyError:
            return JsonResponse(code="999995", msg="参数有误！")

    def post(self, request):
        """
        添加Host
        :param request:
        :return:
        """
        data = JSONParser().parse(request)
        result = self.parameter_check(data)
        if result:
            return result
        try:
            if data["project_id"] is None:
                data["project_id"] = 1
            obj = Project.objects.get(id=data["project_id"])
            if not request.user.is_superuser and obj.user.is_superuser:
                return JsonResponse(code="999983", msg="无操作权限！")
        except ObjectDoesNotExist:
            return JsonResponse(code="999995", msg="项目不存在！")
        pro_data = ProjectSerializer(obj)
        if not pro_data.data["status"]:
            return JsonResponse(code="999985", msg="该项目已禁用")
        obi = Server.objects.filter(name=data["name"], project=data["project_id"])
        if obi:
            return JsonResponse(code="999997", msg="存在相同名称！")
        else:
            serializer = ServerSerializer(data=data)
            with transaction.atomic():
                if serializer.is_valid():
                    # 外键project_id
                    serializer.save(project=obj)
                    # 记录动态
                    record_dynamic(project=data["project_id"],
                                   _type="添加", operationObject="域名", user=request.user.pk, data=data["name"])
                    return JsonResponse(data={
                        "host_id": serializer.data.get("id")
                    }, code="0", msg="成功！")
                return JsonResponse(code="999998", msg="失败！")


class UpdateHost(APIView):
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
                return JsonResponse(code="999995", msg="参数有误！")
            # 必传参数 name, host
            if not data["name"] or not data["host"]:
                return JsonResponse(code="999995", msg="参数有误！")
        except KeyError:
            return JsonResponse(code="999995", msg="参数有误！")

    def post(self, request):
        """
        修改host域名
        :param request:
        :return:
        """
        data = JSONParser().parse(request)
        result = self.parameter_check(data)
        if result:
            return result
        try:
            if data["project_id"] is None:
                data["project_id"]=1
            pro_data = Project.objects.get(id=data["project_id"])
            if not request.user.is_superuser and pro_data.user.is_superuser:
                return JsonResponse(code="999983", msg="无操作权限！")
        except ObjectDoesNotExist:
            return JsonResponse(code="999995", msg="项目不存在！")
        pro_data = ProjectSerializer(pro_data)
        if not pro_data.data["status"]:
            return JsonResponse(code="999985", msg="该项目已禁用")
        try:
            obi = Server.objects.get(id=data["id"])
        except ObjectDoesNotExist:
            return JsonResponse(code="999992", msg="host不存在！")
        host_name = Server.objects.filter(name=data["name"]).exclude(id=data["id"])
        if len(host_name):
            return JsonResponse(code="999997", msg="存在相同名称！")
        else:
            serializer = ServerSerializer(data=data)
            with transaction.atomic():
                if serializer.is_valid():
                    # 外键project_id
                    serializer.update(instance=obi, validated_data=data)
                    # 记录动态
                    record_dynamic(project=data["project_id"],
                                   _type="修改", operationObject="域名", user=request.user.pk, data=data["name"])
                    return JsonResponse(code="0", msg="成功！")
                return JsonResponse(code="999998", msg="失败！")


class DelHost(APIView):
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
                for i in data["ids"]:
                    if not isinstance(i, int):
                        return JsonResponse(code="999995", msg="参数有误！")
                return JsonResponse(code="999995", msg="参数有误！")
        except KeyError:
            return JsonResponse(code="999995", msg="参数有误！")

    def post(self, request):
        """
        删除域名
        :param request:
        :return:
        """
        data = JSONParser().parse(request)
        result = self.parameter_check(data)
        if result:
            return result
        try:
            if data["project_id"] is None:
                data["project_id"]=1
            pro_data = Project.objects.get(id=data["project_id"])
            if not request.user.is_superuser and pro_data.user.is_superuser:
                return JsonResponse(code="999983", msg="无操作权限！")
        except ObjectDoesNotExist:
            return JsonResponse(code="999995", msg="项目不存在！")
        pro_data = ProjectSerializer(pro_data)
        if not pro_data.data["status"]:
            return JsonResponse(code="999985", msg="该项目已禁用")
        try:
            for j in data["ids"]:
                obj = Server.objects.filter(id=j)
                if obj:
                    name = obj[0].name
                    obj.delete()
                    record_dynamic(project=data["project_id"],
                                   _type="删除", operationObject="域名", user=request.user.pk, data=name)
            return JsonResponse(code="0", msg="成功！")
        except ObjectDoesNotExist:
            return JsonResponse(code="999995", msg="项目不存在！")


class DisableProtocol(APIView):
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
            if not isinstance(data["host_id"], int):
                return JsonResponse(code="999995", msg="参数有误！")
        except KeyError:
            return JsonResponse(code="999995", msg="参数有误！")

    def post(self, request):
        """
        禁用host
        :param request:
        :return:
        """
        data = JSONParser().parse(request)
        result = self.parameter_check(data)
        if result:
            return result
        # 查找项目是否存在
        try:
            if data["project_id"] is None:
                data["project_id"]=1
            pro_data = Project.objects.get(id=data["project_id"])
            if not request.user.is_superuser and pro_data.user.is_superuser:
                return JsonResponse(code="999983", msg="无操作权限！")
        except ObjectDoesNotExist:
            return JsonResponse(code="999995", msg="项目不存在！")
        pro_data = ProjectSerializer(pro_data)
        if not pro_data.data["status"]:
            return JsonResponse(code="999985", msg="该项目已禁用")
        try:
            obj = Server.objects.get(id=data["host_id"], project=data["project_id"])
        except ObjectDoesNotExist:
            return JsonResponse(code="999992", msg="host不存在")
        obj.protocol = 'https'
        obj.save()
        record_dynamic(project=data["project_id"],
                       _type="禁用", operationObject="域名", user=request.user.pk, data=obj.name)
        return JsonResponse(code="0", msg="成功！")


class EnableProtocol(APIView):
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
            if not isinstance(data["host_id"], int):
                return JsonResponse(code="999995", msg="参数有误！")
        except KeyError:
            return JsonResponse(code="999995", msg="参数有误！")

    def post(self, request):
        """
        启用
        :param request:
        :return:
        """
        data = JSONParser().parse(request)
        result = self.parameter_check(data)
        if result:
            return result
        # 查找项目是否存在
        try:
            if data["project_id"] is None:
                data["project_id"]=1
            pro_data = Project.objects.get(id=data["project_id"])
            if not request.user.is_superuser and pro_data.user.is_superuser:
                return JsonResponse(code="999983", msg="无操作权限！")
        except ObjectDoesNotExist:
            return JsonResponse(code="999995", msg="项目不存在！")
        pro_data = ProjectSerializer(pro_data)
        if not pro_data.data["status"]:
            return JsonResponse(code="999985", msg="该项目已禁用")
        try:
            obj = Server.objects.get(id=data["host_id"], project=data["project_id"])
        except ObjectDoesNotExist:
            return JsonResponse(code="999992", msg="host不存在")
        obj.protocol = 'http'
        obj.save()
        record_dynamic(project=data["project_id"],
                       _type="禁用", operationObject="域名", user=request.user.pk, data=obj.name)
        return JsonResponse(code="0", msg="成功！")

class DisableHost(APIView):
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
            if not isinstance(data["host_id"], int):
                return JsonResponse(code="999995", msg="参数有误！")
        except KeyError:
            return JsonResponse(code="999995", msg="参数有误！")

    def post(self, request):
        """
        禁用host
        :param request:
        :return:
        """
        data = JSONParser().parse(request)
        result = self.parameter_check(data)
        if result:
            return result
        # 查找项目是否存在
        try:
            if data["project_id"] is None:
                data["project_id"]=1
            pro_data = Project.objects.get(id=data["project_id"])
            if not request.user.is_superuser and pro_data.user.is_superuser:
                return JsonResponse(code="999983", msg="无操作权限！")
        except ObjectDoesNotExist:
            return JsonResponse(code="999995", msg="项目不存在！")
        pro_data = ProjectSerializer(pro_data)
        if not pro_data.data["status"]:
            return JsonResponse(code="999985", msg="该项目已禁用")
        try:
            obj = Server.objects.get(id=data["host_id"], project=data["project_id"])
        except ObjectDoesNotExist:
            return JsonResponse(code="999992", msg="host不存在")
        obj.status = False
        obj.save()
        record_dynamic(project=data["project_id"],
                       _type="禁用", operationObject="域名", user=request.user.pk, data=obj.name)
        return JsonResponse(code="0", msg="成功！")


class EnableHost(APIView):
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
            if not isinstance(data["host_id"], int):
                return JsonResponse(code="999995", msg="参数有误！")
        except KeyError:
            return JsonResponse(code="999995", msg="参数有误！")

    def post(self, request):
        """
        启用
        :param request:
        :return:
        """
        data = JSONParser().parse(request)
        result = self.parameter_check(data)
        if result:
            return result
        # 查找项目是否存在
        try:
            if data["project_id"] is None:
                data["project_id"]=1
            pro_data = Project.objects.get(id=data["project_id"])
            if not request.user.is_superuser and pro_data.user.is_superuser:
                return JsonResponse(code="999983", msg="无操作权限！")
        except ObjectDoesNotExist:
            return JsonResponse(code="999995", msg="项目不存在！")
        pro_data = ProjectSerializer(pro_data)
        if not pro_data.data["status"]:
            return JsonResponse(code="999985", msg="该项目已禁用")
        try:
            obj = Server.objects.get(id=data["host_id"], project=data["project_id"])
        except ObjectDoesNotExist:
            return JsonResponse(code="999992", msg="host不存在")
        obj.status = True
        obj.save()
        record_dynamic(project=data["project_id"],
                       _type="禁用", operationObject="域名", user=request.user.pk, data=obj.name)
        return JsonResponse(code="0", msg="成功！")
