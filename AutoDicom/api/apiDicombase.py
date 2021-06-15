from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from rest_framework.authentication import TokenAuthentication
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView

from AutoProject.common.api_response import JsonResponse
from ..models import dicom_base, dicom, dicom_relation
from AutoProject.common.api_response import JsonResponse
from AutoProject.models import dictionary
from ..serializers import dicom_base_Serializer, dicom_base_Deserializer
from AutoProject.common.regexUtil import *
from AutoDicom.common.dicomfile import fileUpdate
import threading


logger = logging.getLogger(__name__)  # 这里使用 __name__ 动态搜索定义的 logger 配置，这里有一个层次关系的知识点。


class getBase(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def get(self, request):
        """
        获取基础数据
        :param request:
        :return:
        """
        try:
            page_size = int(request.GET.get("page_size", 20))
            page = int(request.GET.get("page", 1))
        except (TypeError, ValueError):
            return JsonResponse(code="999985", msg="page and page_size must be integer!")
        selecttype = request.GET.get("select_type")
        type = request.GET.get("type")
        remarks = request.GET.get("remarks")
        if type:
            if remarks:
                obi = dicom_base.objects.filter(type=type, remarks=remarks).order_by("remarks")
            elif selecttype:
                obi = dicom_base.objects.filter(type=type, select_type=selecttype).order_by("remarks")
            else:
                obi = dicom_base.objects.filter(type=type).order_by("remarks")
        else:
            obi = dicom_base.objects.all().order_by("-id")
        paginator = Paginator(obi, page_size)  # paginator对象
        total = paginator.num_pages  # 总页数
        try:
            obm = paginator.page(page)
        except PageNotAnInteger:
            obm = paginator.page(1)
        except EmptyPage:
            obm = paginator.page(paginator.num_pages)
        serialize = dicom_base_Serializer(obm, many=True)
        dictobj =dictionary.objects.filter(type="file")
        type =[]
        for j in dictobj:
            type.append(j.key)
        for i in serialize.data:
            try:
                obd = dictionary.objects.get(id=i["predictor"])
                i["predictor"] = obd.value
            except Exception as e:
                i["predictor"] = "Null"
                continue
        return JsonResponse(data={"data": serialize.data,
                                  "type": type,
                                  "page": page,
                                  "total": total
                                  }, code="0", msg="成功")


class AddbaseData(APIView):
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
            if not data["remarks"] or not data["type"]  or not data['predictor']:
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

        data["other"] = "0"
        data["status"] = False
        data["content"] = "/files1/DICOM/"+str(data.get("type"))+"/"+str(data.get("remarks"))
        remarks = data["remarks"]
        result = self.parameter_check(data)
        if result:
            return result

        path = str(data["content"])
        basedata = dicom_base.objects.filter(content=path).count()
        if basedata == 0:
            basedata = dicom_base.objects.create(**data)
            return JsonResponse(code="0", msg="成功")
        else:
            return JsonResponse(code="999", msg=" 该类型下已经存在该病种，请更换病种名称")

class getResult(APIView):
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
            if not data["file_path"]:
                return JsonResponse(code="999996", msg="还未上传数据，请先上传数据！")
        except KeyError:
            return JsonResponse(code="999996", msg="还未上传数据，请先上传数据！")

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
        path = str(data["file_path"])[2:]
        relation = dicom_relation.objects.filter(old_path__contains=path)
        if relation.exists() is False:
            return JsonResponse(code="999", msg="处理中，请稍后查询")
        else:
            res = {}
            for i in list(relation):
                if i.success_uid is None:
                    res[i.fail_uid] = '已存在'
                else:
                    res[i.success_uid] = '成功'
            return JsonResponse(code="0", msg=res)

class UpdatebaseData(APIView):
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
            if not data["content"] or not data["type"] or not data["predictor"]:
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
        #
        try:
            baseobj = dicom_base.objects.get(id=data["id"])
        except ObjectDoesNotExist:
            return JsonResponse(code="999995", msg="数据不存在！")
        # 查找是否相同名称的项目
        name = dicom_base.objects.filter(content=data["content"]).exclude(id=data["id"])
        if len(name):
            return JsonResponse(code="999997", msg="存在相同内容数据")
        else:
            serializer = dicom_base_Deserializer(data=data)
            try:
                obj = dicom.objects.filter(fileid=data["id"])
                for i in obj:
                    i.diseases =data["remarks"]
                    i.save()
            except Exception as e:
                return JsonResponse(code="999998", msg="失败")
            with transaction.atomic():
                if serializer.is_valid():
                    # 修改数据
                    serializer.update(instance=baseobj, validated_data=data)
                    return JsonResponse(code="0", msg="成功")
                else:
                    return JsonResponse(code="999998", msg="失败")


class Delbasedata(APIView):
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
                    dicom.objects.filter(fileid=j).delete()
                except Exception as e:
                    logger.error("删除dicom表数据失败")
                dicom_base.objects.filter(id=j).delete()
            return JsonResponse(code="0", msg="成功")
        except ObjectDoesNotExist:
            return JsonResponse(code="999995", msg="项目不存在！")


class Disablebase(APIView):
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
            obj = dicom_base.objects.get(id=data["id"])
            obj.status = False
            obj.save()
            return JsonResponse(code="0", msg="成功")
        except ObjectDoesNotExist:
            return JsonResponse(code="999995", msg="项目不存在！")


class Enablebase(APIView):
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
            obj = dicom_base.objects.get(id=data["id"])
            obj.status = True
            obj.save()

            return JsonResponse(code="0", msg="成功")
        except ObjectDoesNotExist:
            return JsonResponse(code="999995", msg="项目不存在！")


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
            # 环境 类型 online，QualityControl
            if data["service"] not in ["staging", "QualityControl"]:
                return JsonResponse(code="999996", msg="service参数有误！staging，QualityControl")

        except KeyError:
            return JsonResponse(code="999996", msg="参数有误！")

class getDicomfile(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def get(self, request):
        """
        获取基础数据
        :param request:
        :return:
        """
        # 创建线程
        thread_fake_folder = threading.Thread(target=fileUpdate,
                                              args=(request.GET.get("id"),))
        # 启动线程
        thread_fake_folder.start()
        return JsonResponse( code="0", msg="成功")
