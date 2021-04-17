from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from rest_framework.authentication import TokenAuthentication
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView

from AutoProject.common.api_response import JsonResponse
from ..models import dicom_group, dicom, dicom_group_detail, dicom_base
from AutoProject.common.api_response import JsonResponse
from AutoProject.models import dictionary
from ..serializers import dicomGroup_Serializer, dicomGroup_detail_Deserializer
from AutoProject.common.regexUtil import *
from AutoDicom.common.dicomfile import fileUpdate
import threading


logger = logging.getLogger(__name__)  # 这里使用 __name__ 动态搜索定义的 logger 配置，这里有一个层次关系的知识点。

class getGroupBase(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def get(self, request):
        """
        获取所以组信息
        返回到前端 级联查询
        例：
        options: [{
          value: 'zhinan',
          label: '指南',
          children: [{
            value: 'shejiyuanze',
            label: '设计原则',
            children: [{
              value: 'yizhi',
              label: '一致'
            }, {
              value: 'fankui',
              label: '反馈'
            }, {
              value: 'xiaolv',
              label: '效率'
            }, {
              value: 'kekong',
              label: '可控'
            }]
          }
        :param request:
        :return:
        """
        groupChildren = {}
        groupOptions = []
        try:
            baseObj = dicom_base.objects.filter(status=True).order_by("-id")
            for i in baseObj:
                if groupChildren.__contains__(i.type) is False:
                    children = {
                        "value": i.id,
                        "label": i.remarks
                    }
                    groupChildren[i.type] = [children]
                else:
                    groupChildren[i.type].append({
                        "value": i.id,
                        "label": i.remarks
                    })
        except Exception as e:
            logger.error("查询dicom文件报错：{}".format(e))
        try:
            groupChildren["虚拟组"] = []
            for i in dicom_group.objects.filter(status=True).order_by("-id"):
                groupChildren["虚拟组"].append({
                    "value": i.id,
                    "label": i.name
                })
        except Exception as e:
            logger.error("查询虚拟组报错：{}".format(e))

        for k, v in groupChildren.items():
            groupOptions.append({
                "value": k,
                "label": k,
                "children": v
            })

        return JsonResponse(data={"groupOptions": groupOptions}, code="0", msg="成功")


class getGroup(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def get(self, request):
        """
        获取组数据
        :param request:
        :return:
        """
        try:
            page_size = int(request.GET.get("page_size", 20))
            page = int(request.GET.get("page", 1))
        except (TypeError, ValueError):
            return JsonResponse(code="999985", msg="page and page_size must be integer!")
        name = request.GET.get("name")
        remark = request.GET.get("remark")
        if name:
            obi = dicom_group.objects.filter(name=name).order_by("-id")
        elif remark:
            obi = dicom_group.objects.filter(remark=remark).order_by("-id")
        else:
            obi = dicom_group.objects.all().order_by("-id")
        paginator = Paginator(obi, page_size)  # paginator对象
        total = paginator.num_pages  # 总页数
        try:
            obm = paginator.page(page)
        except PageNotAnInteger:
            obm = paginator.page(1)
        except EmptyPage:
            obm = paginator.page(paginator.num_pages)
        serialize = dicomGroup_Serializer(obm, many=True)
        return JsonResponse(data={"data": serialize.data,
                                  "page": page,
                                  "total": total
                                  }, code="0", msg="成功")

class GroupInfo(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def get(self, request):
        """
        获取组详细数据
        :param request:
        :return:
        """
        info = []
        groupInfo = []
        groupId = request.GET.get("groupId")

        # 查询全部 dicom 数据 key dicom 表 ID label 为 patientid 加 remark
        dmObj = dicom.objects.filter(status=True).order_by("diseases")
        for i in dmObj:
            info.append({
                "key": i.id,
                "label": "{0}-{1}".format(i.patientid, i.remark)
            })

        # 查询已选择的 组内数据
        if groupId:
            groupObj = dicom_group_detail.objects.filter(group__id=groupId)
            for j in groupObj:
                groupInfo.append(j.dicom_id)

        return JsonResponse(data={"info": info,
                                  "groupData": groupInfo
                                  }, code="0", msg="成功")


class AddGroup(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def parameter_check(self, data):
        """
        验证参数
        :param data:
        :return:
        """
        try:
            # 必传参数 name
            if not data["name"]:
                return JsonResponse(code="999996", msg="必传参数 name 参数有误！")

        except KeyError:
            return JsonResponse(code="999996", msg="参数有误！")

    def post(self, request):
        """
        新增组数据
        :param request:
        :return:
        """
        data = JSONParser().parse(request)
        result = self.parameter_check(data)
        if result:
            return result
            # 查找是否相同名称的组
        name = dicom_group.objects.filter(name=data["name"])
        if len(name):
            return JsonResponse(code="999997", msg="存在相同组名数据")
        group = dicomGroup_Serializer(data=data)

        with transaction.atomic():
            group.is_valid()
            group.save()
            groupID = group.data.get("id")
        try:
           for i in data["groupData"]:
               detail = dicomGroup_detail_Deserializer(data={
                   "group": groupID,
                   "dicom": int(i)
               })
               with transaction.atomic():
                   detail.is_valid()
                   detail.save()
        except Exception as e:
            logger.error("增加group detail 数据失败，报错：{}".format(e))
            return JsonResponse(code="999995", msg="新增失败：{}".format(e))
        return JsonResponse(code="0", msg="成功")

class UpdateGroup(APIView):
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
            # 必传参数 name
            if not data["name"]:
                return JsonResponse(code="999996", msg="参数有误 必传参数  name！")

        except KeyError:
            return JsonResponse(code="999996", msg="参数有误！")

    def post(self, request):
        """
        修改组
        :param request:
        :return:
        """
        data = JSONParser().parse(request)
        result = self.parameter_check(data)
        if result:
            return result
        groupId = data["id"]
        try:
            Groupobj = dicom_group.objects.get(id=groupId)
        except ObjectDoesNotExist:
            return JsonResponse(code="999995", msg="组不存在！")
        # 查找是否相同名称的组
        name = dicom_group.objects.filter(name=data["name"]).exclude(id=groupId)
        if len(name):
            return JsonResponse(code="999997", msg="存在相同组名数据")
        else:
            serializer = dicomGroup_Serializer(data=data)
            with transaction.atomic():
                if serializer.is_valid():
                    # 修改数据
                    serializer.update(instance=Groupobj, validated_data=data)
            try:
                obj = dicom_group_detail.objects.filter(group__id=groupId)
                for i in obj:
                    i.delete()
                for j in data["groupData"]:
                    detail = dicomGroup_detail_Deserializer(data={
                        "group": groupId,
                        "dicom": int(j)
                    })
                    with transaction.atomic():
                        detail.is_valid()
                        detail.save()
            except Exception as e:
                return JsonResponse(code="999998", msg="失败:{}".format(e))
            return JsonResponse(code="0", msg="成功")


class DelGroup(APIView):
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
                    groupObj = dicom_group_detail.objects.filter(group__id=data["id"])
                    for i in groupObj:
                        i.delete()
                except Exception as e:
                    logger.error("删除数据失败：{}".format(e))
                obj = dicom_group.objects.get(id=j)
                obj.delete()
            return JsonResponse(code="0", msg="成功")
        except ObjectDoesNotExist:
            return JsonResponse(code="999995", msg="项目不存在！")


class DisableGroup(APIView):
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
            obj = dicom_group.objects.get(id=data["id"])
            obj.status = False
            obj.save()
            return JsonResponse(code="0", msg="成功")
        except ObjectDoesNotExist:
            return JsonResponse(code="999995", msg="项目不存在！")


class EnableGroup(APIView):
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
            obj = dicom_group.objects.get(id=data["id"])
            obj.status = True
            obj.save()

            return JsonResponse(code="0", msg="成功")
        except ObjectDoesNotExist:
            return JsonResponse(code="999995", msg="项目不存在！")
