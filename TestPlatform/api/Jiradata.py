import logging

from django.core.exceptions import ObjectDoesNotExist
from rest_framework.authentication import TokenAuthentication
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from TestPlatform.common.api_response import JsonResponse
from TestPlatform.common.jiraData import Jiradata
from TestPlatform.serializers import ProjectDeserializer
from TestPlatform.models import test_report

logger = logging.getLogger(__name__)  # 这里使用 __name__ 动态搜索定义的 logger 配置，这里有一个层次关系的知识点。



class jira_figure(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def parameter_check(self, data):
        """
        验证参数
        :param data:
        :return:
        """
        try:
            # 必传参数 service,system,module,lang,id,
            if not data["service"] or not data["project"] :
                return JsonResponse(code="999996", msg="必传参数有误！")
            # type 类型 Web， App
            if data["service"] not in ["CoinNess-APP-缺陷","Boimind-APP-缺陷","故障", "H5 Main-缺陷","Server-缺陷","线上事故", "线上问题"]:
                return JsonResponse(code="999996", msg="问题类型参数有误！ 应 CoinNess-APP-缺陷、Boimind-APP-缺陷、故障")
            # type 类型 Web， App
            if data["project"] not in ["BUG", "ONLINE"]:
                return JsonResponse(code="999996", msg="类型参数有误！ BUG 、ONLINE")
        except KeyError:
            return JsonResponse(code="999996", msg="参数有误！")

    def post(self, request,*args, **kwargs):
        """
        查詢缺陷
        :param request:
        :return:
        project,platform,sprint_version,starttime,days
        """

        # service = request.GET.get("service")
        # tag_type = request.GET.get("type")
        # rid = request.GET.get("rid")
        # set_tag = request.GET.get("tag")

        data_result = JSONParser().parse(request)
        result = self.parameter_check(data_result)

        if result:
            return result

        project=data_result["project"]
        service=data_result["service"]
        starttime=data_result["starttime"]
        days=data_result["days"]
        status =data_result["status"]
        component =data_result["component"]
        priority =data_result["priority"]

        # 判断版本
        if data_result["sprint_version"] =="":
            d = test_report.objects.get(type=1)
            if service=="Boimind-APP-缺陷":
                sprint_version = d.test_version
            else:
                sprint_version = d.cns_version

        try:
            data = Jiradata().bug_create_solution(project,service,sprint_version,starttime,days,status,component,priority)
            solution_state = Jiradata().bug_solution_state(project,service,sprint_version,starttime,days,status,component,priority)

            if data is False or solution_state is False:

                return JsonResponse(code="999996", msg="数据有误")
            else:
                return JsonResponse(code="0", msg="Success",data={
                                  "figure_list": data,
                                  "solution_state": solution_state
                })

        except ObjectDoesNotExist:
            return JsonResponse(code="999998", msg="未知错误")


class jiradata(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def parameter_check(self, data):
        """
        验证参数
        :param data:
        :return:
        """
        try:
            # 必传参数 service,system,module,lang,id,
            if not data["service"] or not data["project"] or not data["sprint_version"]:
                return JsonResponse(code="999996", msg="必传参数有误！")
            # type 类型 Web， App
            if data["service"] not in ["CoinNess-APP-缺陷", "Boimind-APP-缺陷", "故障", "H5 Main-缺陷", "Server-缺陷", "线上事故", "线上问题"]:
                return JsonResponse(code="999996", msg="问题类型参数有误！ 应 CoinNess-APP-缺陷、Boimind-APP-缺陷、故障")
            # type 类型 Web， App
            if data["project"] not in ["BUG", "ONLINE"]:
                return JsonResponse(code="999996", msg="类型参数有误！ BUG 、ONLINE")
        except KeyError:
            return JsonResponse(code="999996", msg="参数有误！")

    def post(self, request, *args, **kwargs):
        """
        查詢修改tag
        :param request:
        :return:
        project,platform,sprint_version,starttime,days
        """

        # service = request.GET.get("service")
        # tag_type = request.GET.get("type")
        # rid = request.GET.get("rid")
        # set_tag = request.GET.get("tag")

        data = JSONParser().parse(request)
        result = self.parameter_check(data)

        if result:
            return result

        try:
            search_bug = Jiradata().search_bug_total(data["project"], data["service"], data["sprint_version"], data["starttime"],
                                                data["days"], data["status"], data["component"],data["priority"])
            if search_bug is False :
                return JsonResponse(code="999996", msg="数据有误")
            else:
                return JsonResponse(code="0", msg="Success", data=search_bug)

        except ObjectDoesNotExist:
            return JsonResponse(code="999998", msg="未知错误")

class todo(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def get(self, request,*args, **kwargs):
        """
        查詢待办事项
        :param request:
        :return:
        user
        """

        user = request.GET.get("user")

        try:
            # data = Jiradata().Pending(user)
            data =[10,9,4]
            return JsonResponse(code="0", msg="Success",data={
                                  "total": data
                })

        except ObjectDoesNotExist:
            return JsonResponse(code="999998", msg="未知错误")