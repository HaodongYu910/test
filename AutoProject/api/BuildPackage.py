import logging
import os
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from rest_framework.authentication import TokenAuthentication
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView

from AutoProject.common.api_response import JsonResponse
from AutoProject.common.common import record_dynamic
from AutoProject.models import build_package, build_package_detail, uploadfile, Token
from AutoProject.serializers import build_packageSerializer, build_packageDeserializer, build_package_detailSerializer
from ..common.jenkins_api import JenkinsApi

logger = logging.getLogger(__name__)  # 这里使用 __name__ 动态搜索定义的 logger 配置，这里有一个层次关系的知识点。


class BuildStatus(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def get(self, request):
        """
        变更构建状态
        :param request:
        :return:
        """
        try:
            build_id = int(request.GET.get("build_id"))
            build_status = int(request.GET.get("status"))
        except (TypeError, ValueError):
            return JsonResponse(code="999985", msg="build_id must be integer!")

        try:
            obj = build_package.objects.get(id=build_id)
            obj.packStatus = build_status
            obj.save()
        except (TypeError, ValueError):
            return JsonResponse(code="999985", msg="修改失败!" )

        return JsonResponse(code="0", msg="成功")


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
            obi = build_package.objects.filter(name__contains=name, status=True).order_by("-id")
        else:
            obi = build_package.objects.filter(status=True).order_by("-id")
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
            i["packStatus"] = i["packStatus"].split(",")[1]

        return JsonResponse(data={"data": serialize.data,
                                  "page": page,
                                  "total": total
                                  }, code="0", msg="成功")


class BuildDetail(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def get(self, request):
        """
        获取构建历史详情
        :param request:
        :return:
        """
        try:
            build_id = int(request.GET.get("build_id"))
        except (TypeError, ValueError):
            return JsonResponse(code="999985", msg="build_id must be integer!")
        obj = build_package_detail.objects.filter(build__id=build_id).order_by("-id")

        serialize = build_package_detailSerializer(obj, many=True)

        return JsonResponse(data={"data": serialize.data
                                  }, code="0", msg="成功")


class BuildDetailStatus(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def get(self, request):
        """
        获取构建详情状态
        :param request:
        :return:
        jobStatus：'pending'  构建中
                   'SUCCESS'  成功
                   'FAILURE'  失败
                   'ABORTED'  取消


        """
        try:
            build_id = int(request.GET.get("build_id"))
        except (TypeError, ValueError):
            return JsonResponse(code="999985", msg="build_id must be integer!")
        try:

            obj = build_package.objects.get(id=build_id)
            job = JenkinsApi()
            jobStatus = job.buildStatus(obj.git.jenkins_job, obj.job)
            packStatus = obj.packStatus.split(",")
            code = "0"
            if jobStatus == 'SUCCESS':
                data = {
                    "step": packStatus[0],
                    "Status": jobStatus,
                    "progress": 100
                }
            elif jobStatus is None:
                data = {
                    "step": packStatus[0],
                    "Status": 'pending',
                    "progress":  job.speedProgress(obj.git.jenkins_job, obj.job)
                }

            else:
                data = {"step": packStatus[0]}
                code = "999981"

            return JsonResponse(data=data, code=code, msg="成功" )

        except Exception as e:
            return JsonResponse(code="999984", msg=f"获取失败:{e}")

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
            if not data["name"] or not data["git"]:
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
        data["packStatus"] = '0,0'
        build_package_serializer = build_packageDeserializer(data=data)

        try:
            build_package.objects.get(name=data["name"])
            return JsonResponse(code="999997", msg="存在相同名称")
        except ObjectDoesNotExist:
            with transaction.atomic():
                if build_package_serializer.is_valid():
                    # 保持新项目
                    build_package_serializer.save()
                    if data['file_id']:
                        uploadObj = uploadfile.objects.get(id=data['file_id'])
                        uploadObj.fileid = build_package_serializer.data.get("id")
                        uploadObj.save()
                        #os.system(f"rclone sync {uploadObj.fileurl} oss://minio/biomind-ha-se/Biomind-Viewer-Web/")
                    return JsonResponse(data={
                        "build_id": build_package_serializer.data.get("id")
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
            # 校验build_id类型为int
            if not data["build_id"]:
                return JsonResponse(code="999996", msg="build_id 参数有误！")
            # 必传参数 branch
            if not data["name"] or not data["branch"]:
                return JsonResponse(code="999996", msg="branch name 参数有误！")

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
            obj = build_package.objects.get(id=data["build_id"])
            # if not request.user.is_superuser and obj.user.is_superuser:
            #     return JsonResponse(code="999983", msg="无操作权限！")
        except ObjectDoesNotExist:
            return JsonResponse(code="999995", msg="数据不存在！")
        # 查找是否相同名称的项目
        data["user_id"] = Token.objects.get(key=data["user_id"]).user_id
        build_name = build_package.objects.filter(name=data["name"]).exclude(id=data["build_id"])

        if len(build_name) > 1:
            return JsonResponse(code="999997", msg="存在相同构建名称")
        else:
            serializer = build_packageDeserializer(data=data)
            with transaction.atomic():
                if serializer.is_valid():
                    # 修改项目
                    serializer.update(instance=obj, validated_data=data)
                    if data['file_id']:
                        uploadObj = uploadfile.objects.get(id=data['file_id'])
                        uploadObj.fileid = serializer.data.get("id")
                        uploadObj.save()
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
            # 校验build_id类型为int
            if not data["build_id"]:
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
            obj = build_package.objects.get(id=data["build_id"])
            # if not request.user.is_superuser and obj.user.is_superuser:
            #     return JsonResponse(code="999983", msg=str(obj) + "无操作权限！")
            obj.status = False
            obj.save()
            return JsonResponse(code="0", msg="成功")
        except ObjectDoesNotExist:
            return JsonResponse(code="999995", msg="数据不存在！")


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
        # 查找构建是否存在
        try:
            obj = build_package.objects.get(id=data["build_package_id"])
            # 停止构建
            jenkins = JenkinsApi()
            jenkins.stop_job(obj.git.jenkins, obj.job)
            # if not request.user.is_superuser and obj.user.is_superuser:
            #     return JsonResponse(code="999983", msg=str(obj) + "无操作权限！")
            obj.packStatus = '0,0'
            obj.build_status = False
            obj.save()
            # record_dynamic(project=obj.Project_id, module='devops',
            #                _type="停止构建", operationObject="持续集成",
            #                user=1, data=f"停止构建：{obj.name}-{obj.service}-{obj.branch}")
            return JsonResponse(code="0", msg="成功")
        except ObjectDoesNotExist:
            return JsonResponse(code="999995", msg="构建不存在！")


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
        # 查找构建是否存在
        try:
            # if not request.user.is_superuser and obj.user.is_superuser:
            #     return JsonResponse(code="999983", msg=str(obj) + "无操作权限！")
            obj = build_package.objects.get(id=data["build_package_id"])
            param_dict = {'BRANCH': obj.branch, 'build_id': obj.id}

            try:
                jenkins = JenkinsApi()
                job = jenkins.build_job(obj.git.jenkins, param_dict)
                obj.job = job
                obj.packStatus = '1,1'
                obj.build_status = True
                obj.save()
                build_package_detail.objects.create(**{'name': obj.name, 'service': obj.git.name, 'code': obj.code,
                                                       'branch': obj.branch, 'type': obj.type, 'build_id': obj.id,
                                                       'Host_id': obj.Host_id, 'user_id': obj.user_id, 'job': job,
                                                       'packStatus': obj.packStatus, 'status': True})

                # record_dynamic(project=obj.Project_id, module='devops',
                #                _type="构建", operationObject="持续集成", user=request.user.pk,
                #                data=f"构建：{obj.name}-{obj.service}-{obj.branch}")
            except KeyError:
                return JsonResponse(code="999991", msg="保存记录失败！")
            return JsonResponse(code="0", msg="成功")
        except Exception as e:
            return JsonResponse(code="999995", msg="构建失败！")
