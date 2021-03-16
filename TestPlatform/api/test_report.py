# Create your views here.

from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from TestPlatform.common.common import record_dynamic

from TestPlatform.models import test_report,test_risk
from TestPlatform.serializers import test_risk_Serializer,test_risk_Deserializer,test_report_Deserializer,test_report_Serializer
from rest_framework.authentication import TokenAuthentication
from TestPlatform.common.api_response import JsonResponse
from HtmlTemplate.testreport_html import report_html


class loadReport(APIView):
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
        type = request.GET.get("type")
        if type:
            obi = test_report.objects.filter(type__contains=type).order_by("-report_id")
        else:
            obi = test_report.objects.all().order_by("report_id")
        paginator = Paginator(obi, page_size)  # paginator对象
        total = paginator.num_pages  # 总页数
        try:
            obm = paginator.page(page)
        except PageNotAnInteger:
            obm = paginator.page(1)
        except EmptyPage:
            obm = paginator.page(paginator.num_pages)
        serialize = test_report_Serializer(obm, many=True)
        return JsonResponse(data={"data": serialize.data,
                                  "page": page,
                                  "total": total
                                  }, code="0", msg="成功")


class Addreport(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def parameter_check(self, data):
        """
        验证参数
        :param data:
        :return:
        """
        try:
            # 必传参数
            if not data["test_version"] or not data["cns_version"] or not data["type"] or not data["title"]:
                return JsonResponse(code="999996", msg="必传参数有误！")
        except KeyError:
            return JsonResponse(code="999996", msg="参数有误！")

    def post(self, request):
        """
        新增版本报告
        :param request:
        :return:
        """
        data = JSONParser().parse(request)
        content=[]
        result = self.parameter_check(data)
        if result:
            return result
        testreport_serializer = test_report_Serializer(data=data)
        with transaction.atomic():
            if testreport_serializer.is_valid():
                testreport_serializer.save()
                return JsonResponse(data={'True'
                                          }, code="0", msg="成功")
            else:
                return JsonResponse(code="999998", msg="失败")

class Updatereport(APIView):
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
            if not isinstance(data["report_id"], int):
                return JsonResponse(code="999996", msg="参数有误！")
            # 必传参数
            if not data["test_version"] or not data["cns_version"] or not data["type"]:
                return JsonResponse(code="999996", msg="参数有误！")
        except KeyError:
            return JsonResponse(code="999996", msg="参数有误！")

    def post(self,request):
        """
        修改信息
        :param request:
        :return:
        """
        data = JSONParser().parse(request)
        result = self.parameter_check(data)
        if result:
            return result
        # 查找项目是否存在
        try:
            obj = test_report.objects.get(report_id=data["report_id"])
        except ObjectDoesNotExist:
            return JsonResponse(code="999995", msg="数据不存在！")

        serializer = test_report_Deserializer(data=data)
        with transaction.atomic():
            if serializer.is_valid():
                # 修改信息
                serializer.update(instance=obj, validated_data=data)
                return JsonResponse(code="0", msg="成功")
            else:
                 return JsonResponse(code="999998", msg="失败")

class Delreport(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def parameter_check(self, data):
        """
        校验参数
        :param data:
        :return:
        """
        try:
            # 校验report_id类型为int
            if not isinstance(data["ids"], list):
                return JsonResponse(code="999996", msg="参数有误！")
            for i in data["ids"]:
                if not isinstance(i, int):
                    return JsonResponse(code="999996", msg="参数有误！")
        except KeyError:
            return JsonResponse(code="999996", msg="参数有误！")

    def post(self, request):
        """
        删除邮件配置
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
                    obj = test_report.objects.get(report_id=i)
                    # if not request.user.is_superuser and obj.user.is_superuser:
                    #     return JsonResponse(code="999983", msg=str(obj)+"无操作权限！")
                except ObjectDoesNotExist:
                    return JsonResponse(code="999995", msg="数据不存在！")
            for j in data["ids"]:
                obj = test_report.objects.filter(report_id=j)
                obj.delete()
                # my_user_cron = CronTab(user=True)
                # my_user_cron.remove_all(comment=j)
                # my_user_cron.write()
            return JsonResponse(code="0", msg="成功")
        except ObjectDoesNotExist:
            return JsonResponse(code="999995", msg="数据不存在！")

class Sendreport(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def parameter_check(self, data):
        """
        验证参数
        :param data:
        :return:
        """
        try:
            # 必传参数
            if not data["test_version"] or not data["cns_version"] or not data["type"] or not data["title"]:
                return JsonResponse(code="999996", msg="必传参数有误！")
        except KeyError:
            return JsonResponse(code="999996", msg="参数有误！")

    def post(self, request):
        """
        新增版本报告
        :param request:
        :return:
        """
        data = JSONParser().parse(request)
        content=[]
        result = self.parameter_check(data)
        if result:
            return result
        testreport_serializer = test_report_Serializer(data=data)
        with transaction.atomic():
            if testreport_serializer.is_valid():
                testreport_serializer.save()
                report_html(data["test_version"],data["cns_version"],content)
                return JsonResponse(data={'True'
                                          }, code="0", msg="成功")
            else:
                return JsonResponse(code="999998", msg="失败")

class Testrisk(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def get(self,request,format=None):
        project_id = request.GET.get("project_id")
        data = test_risk.objects.filter(project_id__contains=project_id).order_by("update_time")
        serializer = test_risk_Serializer(data, many=True)

        return Response(serializer.data)

class Add_test_risk(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def parameter_check(self, data):
        """
        验证参数
        :param data:
        :return:
        """
        try:
            # 必传参数
            if not data["project_id"] or not data["risk"] or not data["solution_status"] or not data["status"]:
                return JsonResponse(code="999996", msg="必传参数有误！")
        except KeyError:
            return JsonResponse(code="999996", msg="参数有误！")


    def post(self, request):
        """
        新增测试风险
        :param request:
        :return:
        """
        data = JSONParser().parse(request)
        result = self.parameter_check(data)
        if result:
            return result
        test_risk_serializer = test_risk_Serializer(data=data)
        with transaction.atomic():
            if test_risk_serializer.is_valid():
                test_risk_serializer.save()
                return JsonResponse(data={'True'
                                          }, code="0", msg="成功")
            else:
                return JsonResponse(code="999998", msg="失败")


class Updatetest_risk(APIView):
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
            if not isinstance(data["risk_id"], int):
                return JsonResponse(code="999996", msg="参数有误！")
            # 必传参数
            if not data["project_id"] or not data["risk"] or not data["solution_status"] or not data["status"]:
                return JsonResponse(code="999996", msg="必传参数有误！")

        except KeyError:
            return JsonResponse(code="999996", msg="参数有误！")

    def post(self, request):
        """
        修改测试风险
        :param request:
        :return:
        """
        data = JSONParser().parse(request)
        result = self.parameter_check(data)
        if result:
            return result
        # 查找项目是否存在
        try:
            obj = test_risk.objects.get(risk_id=data["risk_id"])
            # if not request.user.is_superuser and obj.user.is_superuser:
            #     return JsonResponse(code="999983", msg="无操作权限！")
        except ObjectDoesNotExist:
            return JsonResponse(code="999995", msg="数据不存在！")

        serializer = test_risk_Deserializer(data=data)
        with transaction.atomic():
            if serializer.is_valid():
                # 修改数据
                serializer.update(instance=obj, validated_data=data)
                # 记录动态
                # record_dynamic(project=data["project_id"],
                #                _type="修改", operationObject="项目", user=request.user.pk, data=data["name"])
                return JsonResponse(code="0", msg="成功")
            else:
                return JsonResponse(code="999998", msg="失败")


class DelAutotest_risk(APIView):
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
        删除测试风险
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
                    obj = test_risk.objects.get(risk_id=i)
                    # if not request.user.is_superuser and obj.user.is_superuser:
                    #     return JsonResponse(code="999983", msg=str(obj)+"无操作权限！")
                except ObjectDoesNotExist:
                    return JsonResponse(code="999995", msg="数据不存在！")
            for j in data["ids"]:
                obj = test_risk.objects.filter(risk_id=j)
                obj.delete()
                # my_user_cron = CronTab(user=True)
                # my_user_cron.remove_all(comment=j)
                # my_user_cron.write()
            return JsonResponse(code="0", msg="成功")
        except ObjectDoesNotExist:
            return JsonResponse(code="999995", msg="数据不存在！")

class DisableRisk(APIView):
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
            if not isinstance(data["risk_id"], int):
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
            obj = test_risk.objects.get(id=data["risk_id"])
            if not request.user.is_superuser and obj.user.is_superuser:
                return JsonResponse(code="999983", msg=str(obj) + "无操作权限！")
            obj.status = False
            obj.save()
            record_dynamic(project=data["risk_id"],
                           _type="禁用", operationObject="项目", user=request.user.pk, data=obj.name)
            return JsonResponse(code="0", msg="成功")
        except ObjectDoesNotExist:
            return JsonResponse(code="999995", msg="项目不存在！")


class EnableRisk(APIView):
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
            if not isinstance(data["risk_id"], int):
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
            obj = test_risk.objects.get(id=data["risk_id"])
            if not request.user.is_superuser and obj.user.is_superuser:
                return JsonResponse(code="999983", msg=str(obj) + "无操作权限！")
            obj.status = True
            obj.save()
            record_dynamic(project=data["risk_id"],
                           _type="禁用", operationObject="项目", user=request.user.pk, data=obj.name)
            return JsonResponse(code="0", msg="成功")
        except ObjectDoesNotExist:
            return JsonResponse(code="999995", msg="项目不存在！")
