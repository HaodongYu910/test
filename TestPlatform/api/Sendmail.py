import logging

from django.core.exceptions import ObjectDoesNotExist
from rest_framework.authentication import TokenAuthentication
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from TestPlatform.common.api_response import JsonResponse
from TestPlatform.common.jenkins_api import get_job_details
from TestPlatform.common.download_mail import download
from TestPlatform.common.sendmail import send_mail
from TestPlatform.models import test_report
from HtmlTemplate.test_html import html
from HtmlTemplate.testreport_html import report_html
from django.conf import settings


logger = logging.getLogger(__name__)  # 这里使用 __name__ 动态搜索定义的 logger 配置，这里有一个层次关系的知识点。


class sendmail(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def post(self, request):
        """
        测试邮件
        :param request:
        :return:
        """
        email_cc = []
        receiver =[]
        data = JSONParser().parse(request)


        try:
            if int(data["type"])==0:
                download(data["starttime"],data["endtime"])
            else:

                re = test_report.objects.get(type=int(data["type"]))

                if int(re.type) == 1:
                    Html = html(re.test_version,re.cns_version)
                elif int(re.type) == 2:
                    Html = report_html(re.test_version, re.cns_version,['','','','','',''])
                elif int(re.type) == 3:
                    Html = report_html(re.test_version, re.cns_version)

                if re.receiver == 'Autotest':   # 测试邮件
                   receiver = ['yinhang@bishijie.com', 'yinhang@bishijie.com']
                   email_cc = ['yinhang@bishijie.com', 'yinhang@bishijie.com']
                else: # 正式邮件
                   receiver = ['tech@bishijie.com', 'product@bishijie.com', 'op@bishijie.com',
                                    'yunwei@bishijie.com', 'qa.list@bishijie.com']
                   for i in re.email_cc.split(","):
                       email_cc.append(i)
                # 附件
                # attach_xlsx = 'C:/Users/Hvte/Desktop/coinness1.6 行情测试用例.xlsx'
                # attach_jpg = 'D:/360Downloads/wey.png'
                try:
                    send_mail([settings.MAIL_USER, receiver, email_cc, re.title,Html])
                except KeyError:
                    return JsonResponse(code="999996", msg="参数有误！")

            return JsonResponse(code="0", msg="成功")
        except ObjectDoesNotExist:
            return JsonResponse(code="999998", msg="失败")

class down_load(APIView):
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
            if not data["system"] or not data["client"]or not data["version"]:
                return JsonResponse(code="999996", msg="必传参数有误！")
            # 环境 类型 coinness，bishijie
            if data["system"] not in ["CoinNess", "CoinWorld"]:
                return JsonResponse(code="999996", msg="system参数有误！应为 CoinNess ,CoinWorld")
            # system 类型 Android， iOS
            if data["client"] not in ["Android", "iOS"]:
                return JsonResponse(code="999996", msg="client参数有误！Android,iOS")
            if data["channel"] not in ["Debug", "Release","Huidu","AdHoc","Release"]:
                return JsonResponse(code="999996", msg="client参数有误！Android,iOS")
        except KeyError:
            return JsonResponse(code="999996", msg="参数有误！")

    def post(self, request,*args, **kwargs):
        """
        下载地址
        :param request:
        :return:
        """

        data = JSONParser().parse(request)

        result = self.parameter_check(data)
        if result:
            return result

        try:
            params = get_job_details((data["system"] + '_' + data["client"] + '_Branch_' + data["version"]),data["channel"],data["client"])
            if data["client"] =="iOS":
                url = (
                    "itms-services://?action=download-manifest&url=https://package.bishijie.com/job/{0}_iOS_Branch_{1}/{2}/artifact/Products/{0}.plist").format(
                    data["system"], data["version"], params[0])
            else:
                url = (
                    "http://qa-jenkins.bishijie.com/job/{0}_{1}_Branch_{2}/{3}/artifact/Products/{0}.apk").format(
                    data["system"], data["client"], data["version"], params[0])
            return JsonResponse(code="0", msg="成功",data={"url":url,
                                                              "PUSH_KEY": params[1],
                                                              })
        except ObjectDoesNotExist:
            return JsonResponse(code="999998", msg="失败")



