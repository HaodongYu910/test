from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from rest_framework.authentication import TokenAuthentication
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from AutoTest.common.api_response import JsonResponse

from ..serializers import stress_Deserializer
from AutoDicom.serializers import dicomdata_Deserializer
from ..common.stress import voteData,checkuid
from AutoDicom.common.deletepatients import *
from ..models import stress

logger = logging.getLogger(__name__)  # 这里使用 __name__ 动态搜索定义的 logger 配置


class stressversion(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def get(self, request):
        """
        获取性能测试版本
        :param request:
        :return:
        """
        projectname = request.GET.get("projectname", '晨曦')
        obj = stress.objects.filter(projectname=projectname)
        serialize = stress_Deserializer(obj, many=True)
        # for i in obi.version:
        #     dict = {'key': i, 'value': i}
        #     list.append(dict)
        return JsonResponse(data={"data": serialize.data
                                  }, code="0", msg="成功")

class stressData(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def get(self, request):
        """
        获取性能数据
        :param request:
        :return:
        """
        try:
            page_size = int(request.GET.get("page_size", 20))
            page = int(request.GET.get("page", 1))
        except (TypeError, ValueError):
            return JsonResponse(code="999985", msg="page and page_size must be integer!")
        diseases = request.GET.get("diseases")
        slicenumber = request.GET.get("slicenumber")
        if diseases is not None and slicenumber is None:
            obi = dicom.objects.filter(diseases=diseases, stressstatus__in=(1, 2)).order_by("-id")
        elif diseases is None and slicenumber is not None:
            obi = dicom.objects.filter(slicenumber=slicenumber, stressstatus__in=(1, 2)).order_by("-id")
        else:
            obi = dicom.objects.filter(stressstatus__in=(1,2)).order_by("-id")
        paginator = Paginator(obi, page_size)  # paginator对象
        total = paginator.num_pages  # 总页数
        try:
            obm = paginator.page(page)
        except PageNotAnInteger:
            obm = paginator.page(1)
        except EmptyPage:
            obm = paginator.page(paginator.num_pages)
        serialize = dicomdata_Deserializer(obm, many=True)
        for i in serialize.data:
            dictobj = dictionary.objects.get(id=i["predictor"])
            i["diseases"] = dictobj.value
            if i["stressstatus"] == '2':
                i["benchmarkstatus"] = True
            else:
                i["benchmarkstatus"] = False
        return JsonResponse(data={"data": serialize.data,
                                  "page": page,
                                  "total": total
                                  }, code="0", msg="成功")

class AddStressData(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def parameter_check(self, data):
        """
        添加性能测试数据
        校验参数
        :param data:
        :return:
        """
        try:
            # 必传参数 ids
            if not data["ids"]:
                return JsonResponse(code="999996", msg="参数有误,必传参数 ids！")

        except KeyError:
            return JsonResponse(code="999996", msg="参数ids有误！")

    def post(self, request):
        """
        :param request:
        :return:
        """
        data = JSONParser().parse(request)
        result = self.parameter_check(data)
        if result:
            return result
        try:
            for i in data["ids"]:
                obj = dicom.objects.get(id=i)
                obj.stressstatus = 1
                obj.save()
            return JsonResponse(code="0", msg="成功")
        except ObjectDoesNotExist:
            return JsonResponse(code="999995", msg="数据不存在！")

class SynchroStressData(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def parameter_check(self, data):
        """
        校验参数
        :param data:
        :return:
        """
        try:
            # 必传参数 ids
            if not data["ids"]:
                return JsonResponse(code="999996", msg="参数有误,必传参数 ids！")

        except KeyError:
            return JsonResponse(code="999996", msg="参数ids有误！")

    def post(self, request):
        """
        同步压测数据
        :param request:
        :return:
        """
        data = JSONParser().parse(request)
        result = self.parameter_check(data)
        if result:
            return result
        try:
            kc = login_keycloak(1)
            for i in data["ids"]:
                obj = dicom.objects.get(recordid=i)
                try:
                    checkuid(1, '192.168.1.208', obj.stressid)
                except ObjectDoesNotExist:
                    logger.error("数据问题{0}".format(obj.studyuid))
                obj.graphql, obj.imagecount, obj.slicenumber = voteData(obj.studyuid, '192.168.1.208', obj.diseases, kc)
                obj.save()
            return JsonResponse(code="0", msg="成功")
        except ObjectDoesNotExist:
            return JsonResponse(code="999995", msg="数据不存在！")


class DelStressData(APIView):
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
            if not isinstance(data["ids"], list):
                return JsonResponse(code="999996", msg="参数有误！")
            for i in data["ids"]:
                if not isinstance(i, int):
                    return JsonResponse(code="999996", msg="参数有误！")
        except KeyError:
            return JsonResponse(code="999996", msg="参数有误！")

    def post(self, request):
        """
        删除压测数据
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
                    obj = dicom.objects.get(id=j)
                    obj.stressstatus = 0
                    obj.save()
                except Exception as e:
                    return JsonResponse(code="999998", msg="删除失败")
            return JsonResponse(code="0", msg="成功")
        except ObjectDoesNotExist:
            return JsonResponse(code="999995", msg="数据不存在！")


class DisableBenchmarkStatus(APIView):
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
        禁用基准数据
        :param request:
        :return:
        """
        data = JSONParser().parse(request)
        result = self.parameter_check(data)
        if result:
            return result
        # 查找是否存在
        try:
            obj = dicom.objects.get(id=data["id"])
            obj.stressstatus = 1
            obj.save()
            return JsonResponse(code="0", msg="成功")
        except ObjectDoesNotExist:
            return JsonResponse(code="999995", msg="不存在！")


# Enable 基准数据
class EnableBenchmarkStatus(APIView):
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
        启用基准数据
        :param request:
        :return:
        """
        data = JSONParser().parse(request)
        result = self.parameter_check(data)
        if result:
            return result
        # 查找项目是否存在
        try:
            obj = dicom.objects.get(id=data["id"])
            obj.stressstatus = 2
            obj.save()

            return JsonResponse(code="0", msg="成功")
        except ObjectDoesNotExist:
            return JsonResponse(code="999995", msg="不存在！")


