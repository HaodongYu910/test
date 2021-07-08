from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.authentication import TokenAuthentication
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView


from ..models import  dicom_relation, dicom
from AutoProject.common.api_response import JsonResponse
from AutoProject.models import dictionary
from AutoProject.common.regexUtil import *
from AutoDicom.common.dicomfile import fileUpdate
import threading


logger = logging.getLogger(__name__)  # 这里使用 __name__ 动态搜索定义的 logger 配置，这里有一个层次关系的知识点。



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
            return JsonResponse(code="999", msg="请先上传数据，在查看结果")
        else:
            res = {}
            for i in list(relation):
                if i.success_uid is None:
                    if str(i.fail_uid).count("【检查数据】："):
                        res[i.fail_uid] = '数据类型错误'
                    else:
                        res[i.fail_uid] = '已存在'
                else:
                    res[i.success_uid] = '成功'
            return JsonResponse(code="0", msg=res)


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
        return JsonResponse(code="0", msg="成功")


class DetailDisable(APIView):
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
            if not data["studyuid"]:
                return JsonResponse(code="999996", msg="参数有误！")
        except KeyError:
            return JsonResponse(code="999996", msg="参数有误！")

    def post(self, request):
        """
        禁用数据
        :param request:
        :return:
        """
        data = JSONParser().parse(request)
        result = self.parameter_check(data)
        if result:
            return result
        # 查找是否存在
        try:
            obj = dicom.objects.filter(studyinstanceuid=data["studyuid"])
            obj.status = False
            obj.save()
            return JsonResponse(code="0", msg="成功")
        except ObjectDoesNotExist:
            return JsonResponse(code="999995", msg="数据不存在！")