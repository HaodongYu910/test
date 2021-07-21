from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.conf import settings
from django.db import transaction
from django.db.models import Q

from rest_framework.authentication import TokenAuthentication
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView

from AutoProject.common.api_response import JsonResponse
from AutoProject.serializers import ProjectVersionSerializer, ProjectVersionDeserializer
from ..common.install import InstallThread
from AutoDicom.common.deletepatients import *
from ..models import project_version, Project
import os
logger = logging.getLogger(__name__)  # 这里使用 __name__ 动态搜索定义的 logger 配置


class getVersionInfo(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def get(self, request):
        """
        获取Install 版本
        :param request:
        :return:
        """
        try:
            project_id = request.GET.get("project_id", 1)
            Obj = project_version.objects.filter(~Q(type='-1'), project_id=project_id, status=True).order_by("-id")

            serialize = ProjectVersionSerializer(Obj, many=True)
            return JsonResponse(data={"data": serialize.data}, code="0", msg="成功")
        except (TypeError, ValueError):
            return JsonResponse(code="999985", msg="获取版本失败!")


class getVersion(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def get(self, request):
        """
        获取项目Version 版本
        :param request:
        :return:
        """
        try:
            project_id = request.GET.get("project_id", 1)
            page_size = int(request.GET.get("page_size", 20))
            page = int(request.GET.get("page", 1))
        except (TypeError, ValueError):
            return JsonResponse(code="999985", msg="page and page_size must be integer!")
        version = request.GET.get("version")
        name = request.GET.get("name")
        if version:
            obi = project_version.objects.filter(~Q(type='-1'), version__contains=version, project_id=project_id).order_by("-id")
        elif name:
            obi = project_version.objects.filter(~Q(type='-1'), version__contains=name, project_id=project_id).order_by("-id")
        else:
            obi = project_version.objects.filter(~Q(type='-1'), project_id=project_id).order_by("-id")
        paginator = Paginator(obi, page_size)  # paginator对象
        total = paginator.num_pages  # 总页数
        try:
            obm = paginator.page(page)
        except PageNotAnInteger:
            obm = paginator.page(1)
        except EmptyPage:
            obm = paginator.page(paginator.num_pages)
        serialize = ProjectVersionSerializer(obm, many=True)
        return JsonResponse(data={"data": serialize.data,
                                  "page": page,
                                  "total": total
                                  }, code="0", msg="成功")



class AddVersion(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def parameter_check(self, data):
        """
        验证参数
        :param data:
        :return:
        """
        try:
            # 必传参数 version ,branch, project
            if not data["version"] or not data["branch"] or not data["project"]:
                return JsonResponse(code="999996", msg="参数有误,必传参数 version ,branch, project！")

        except KeyError:
            return JsonResponse(code="999996", msg="参数有误,必传参数 version ,branch, project！")

    def post(self, request):
        """
        新增项目版本数据
        :param request:
        :return:
        """
        data = JSONParser().parse(request)
        result = self.parameter_check(data)
        if result:
            return result
        try:
            package = 1
            obj = project_version.objects.filter(type__in=['1', '-1'], version=data["version"])
            try:
                # 版本打包个数
                vesionCount = int(obj.count())

                if vesionCount > 0:
                    # 历史版本置为失效状态
                    for i in obj:
                        i.status = False
                        i.save()
                    # 当前版本 包名 加 1 存储
                    package = vesionCount + 1
                    data["package_name"] = f"{data['version']}{package}.tgz"
                else:
                    data["package_name"] = f"{data['version']}1.tgz"
            except:
                data["package_name"] = f"{data['version']}1.tgz"
            data["status"] = True
            data["path"] = "oss://biomind/{0}/{1}/{2}".format(
                data["project"], data["type"], data["package_name"])
            try:
                data["project"] = int(Project.objects.get(version=data["project"]).id)
            except ObjectDoesNotExist:
                return JsonResponse(code="999994", msg="项目不存在，请创建项目或联系管理员")
            if "rod" in data["type"]:
                data["type"] = 1

            projectVersion = ProjectVersionDeserializer(data=data)
            with transaction.atomic():
                projectVersion.is_valid()
                projectVersion.save()
            return JsonResponse(code="0", msg="成功", data=package)
        except Exception as e:
            return JsonResponse(code="999995", msg="{0}".format(e))


class UpdateVersion(APIView):
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
            if not isinstance(data["Host_id"], int):
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
            obj = project_version.objects.get(id=data["id"])
        except Exception as e:
            return JsonResponse(code="999995", msg="版本数据不存在！")

        serializer = project_version(data=data)
        with transaction.atomic():
            if serializer.is_valid():
                # 修改数据
                serializer.update(instance=obj, validated_data=data)
                return JsonResponse(code="0", msg="成功")
            else:
                return JsonResponse(code="999998", msg="失败")


class DelVersion(APIView):
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
                    obj = project_version.objects.get(id=j)
                    obj.type = "-1"
                    obj.save()
                    os.system(f"rclone delete {obj.path}")
                except Exception as e:
                    logger.error(f"删除{obj.version}数据失败:{e}")
                    continue
            return JsonResponse(code="0", msg="成功")
        except ObjectDoesNotExist:
            return JsonResponse(code="999995", msg="项目不存在！")


class DisableVersion(APIView):
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
            obj = project_version.objects.get(id=data["id"])
            obj.status = False
            obj.save()

            return JsonResponse(code="0", msg="成功")
        except ObjectDoesNotExist:
            return JsonResponse(code="999995", msg="数据不存在！")


class EnableVersion(APIView):
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
        启用项目版本
        :param request:
        :return:
        """
        data = JSONParser().parse(request)
        result = self.parameter_check(data)
        if result:
            return result
        # 查找项目是否存在
        try:
            obj = project_version.objects.get(id=data["id"])
            obj.status = True
            obj.save()
            return JsonResponse(code="0", msg="成功")
        except ObjectDoesNotExist:
            return JsonResponse(code="999995", msg="项目版本不存在！")


class SaveVersion(APIView):
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
        保存项目版本
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
                    obj = project_version.objects.get(id=j)
                    path = f"/files/History_version/{obj.version}"
                    if os.path.exists(path):
                        os.makedirs(path)
                    os.system(f"rclone copy {obj.path} {path}")
                    obj.type = '2'
                    obj.save()
                    
                except Exception as e:
                    logger.error(f"删除{obj.version}数据失败:{e}")
                    continue
            return JsonResponse(code="0", msg="保存成功")
        except ObjectDoesNotExist:
            return JsonResponse(code="999995", msg="项目版本保存失败！")