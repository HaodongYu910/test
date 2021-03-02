from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db import transaction
from django.db.models import Count

from rest_framework.authentication import TokenAuthentication
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
import threading

from TestPlatform.common.api_response import JsonResponse
from ..serializers import autorecord_Serializer
from TestPlatform.tools.orthanc.deletepatients import *
from ..models import autoui,auto_uirecord
from TestPlatform.models import uploadfile
from AutoUI.common.autouitest import *

logger = logging.getLogger(__name__)  # 这里使用 __name__ 动态搜索定义的 logger 配置


class AutoRecord(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def get(self, request):
        """
        获取UI测试数据显示数据列表
        :param request:
        :return:
        """
        try:
            page_size = int(request.GET.get("page_size", 20))
            page = int(request.GET.get("page", 1))
        except (TypeError, ValueError):
            return JsonResponse(code="999985", msg="page and page_size must be integer!")
        diseases = request.GET.get("diseases")
        autoid = request.GET.get("autoid")

        if request.GET.get("status")=='true':
            status = 1
        elif request.GET.get("status")=='False':
            status = 0
        else:
            status = ''

        if diseases != '' and status != '':
            obi = auto_uirecord.objects.filter(diseases__contains=diseases, status=status, autoid=autoid).order_by("-recordid")
        elif diseases == ''  and status != '':
            obi = auto_uirecord.objects.filter(diseases__contains=diseases,status=status,autoid=autoid).order_by("-recordid")
        else:
            obi = auto_uirecord.objects.filter(autoid=autoid).order_by("-recordid")
        paginator = Paginator(obi, page_size)  # paginator对象
        total = paginator.num_pages  # 总页数
        try:
            obm = paginator.page(page)
        except PageNotAnInteger:
            obm = paginator.page(1)
        except EmptyPage:
            obm = paginator.page(paginator.num_pages)
        serialize = autorecord_Serializer(obm, many=True)
        for i in serialize.data:
            # 求预测时间
            if i['completiontime'] is not None and i['starttime'] is not None:
                completiontime = time.strptime(str(i['completiontime']), "%Y-%m-%d %H:%M:%S")
                starttime = time.strptime(str(i['starttime']), "%Y-%m-%d %H:%M:%S")
                i['time'] = int(time.mktime(completiontime)) - int(time.mktime(starttime))
        return JsonResponse(data={"data": serialize.data,
                                  "page": page,
                                  "total": total
                                  }, code="0", msg="成功")

class getUIReport(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def get(self, request):
        """
        获取错误截图 url
        :param request:
        :return:
        """
        try:
            autoid = request.GET.get("autoid", 0)
        except (TypeError, ValueError):
            return JsonResponse(code="999985", msg="autoid must be integer!")
        data = []
        srcList = {}
        folder = '/home/biomind/Biomind_Test_Platform/static/UI/{}/report/'.format(str(autoid))
        file_names = os.listdir(folder)
        file_names.sort()
        for fn in file_names:
            data.append(fn)
            srcList[fn] = 'http://192.168.1.121/static/UI/{0}/report/{1}'.format(str(autoid),str(fn))
        return JsonResponse(data={"reports": data,
                                  "reportList": srcList}, code="0", msg="成功")

class getUIimage(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def get(self, request):
        """
        获取错误截图 url
        :param request:
        :return:
        """
        try:
            autoid = request.GET.get("autoid", 0)
        except (TypeError, ValueError):
            return JsonResponse(code="999985", msg="autoid must be integer!")
        data = {}
        srcList = []
        folder = '/home/biomind/Biomind_Test_Platform/static/UI/{}/errorimage/'.format(str(autoid))
        file_names = os.listdir(folder)
        file_names.sort()
        for fn in file_names:
            url ='http://192.168.1.121/static/UI/{0}/errorimage/{1}'.format(str(autoid),str(fn))
            data[fn] = url
            srcList.append(url)
        return JsonResponse(data={"fits": data,
                                  "srcList": srcList}, code="0", msg="成功")

class getCaseFile(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def get(self, request):
        """
        获取用例内容
        :param request:
        :return:
        """
        try:
            id = int(request.GET.get("id", 20))
            obj = uploadfile.objects.get(fileid=id)
            with open('{0}/{1}'.format(obj.fileurl,obj.filename), 'r', encoding='utf-8') as f:
                data = f.read()
                f.close()
        except (TypeError, ValueError):
            return JsonResponse(code="999985", msg="page and page_size must be integer!")

        return JsonResponse(data={"data": data
                                  }, code="0", msg="成功")

class UpdateCaseFile(APIView):
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
            if not data["type"] or not data["name"]:
                return JsonResponse(code="999996", msg="参数有误！")

        except KeyError:
            return JsonResponse(code="999996", msg="参数有误！")

    def post(self, request):
        """
        新增用例
        :param request:
        :return:
        """
        data = JSONParser().parse(request)
        result = self.parameter_check(data)
        if result:
            return result
        try:
            id = data["id"]
            obj = uploadfile.objects.get(fileid=id)
            f = open('{0}/{1}'.format(obj.fileurl, obj.filename), 'r', encoding='utf-8')
            data = f.read()
            f.close()
            return JsonResponse(code="0", msg="成功")
        except Exception as e:
            return JsonResponse(code="999995", msg="{0}".format(e))

class Autofigure(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def parameter_check(self, data):
        """
        验证参数
        :param data:
        :return:
        """
        try:
            # 必传参数 version
            if not data["version"]:
                return JsonResponse(code="999996", msg="缺失必要参数,参数 version！")

        except KeyError:
            return JsonResponse(code="999996", msg="参数有误！")

    def post(self, request):
        """
        预测时间 金标准结果
        :param request:
        :return:
        """
        data = JSONParser().parse(request)
        result = self.parameter_check(data)
        if result:
            return result
        try:
            goldrows = []
            goldcolumns =[]
            # if data['version']:
            #     print(1)
            versions = autoui.objects.filter(status=True)
            for i in versions:
                goldcolumns.append(i.version)
                count = auto_uirecord.objects.filter(smokeid=i.id).aggregate(report_nums=Count("report"))
                success = auto_uirecord.objects.filter(smokeid=i.id,report='匹配成功').aggregate(report_nums=Count("report"))
                fail = auto_uirecord.objects.filter(smokeid=i.id, report='匹配失败').aggregate(report_nums=Count("report"))
                histogram = {
                    '版本': i.version,
                    '匹配成功': success["report_nums"],
                    '匹配失败': fail['report_nums'],
                    '预测失败': int(count['report_nums']) - int(success["report_nums"]) - int(fail['report_nums'])
                }
                goldrows.append(histogram)
            return JsonResponse(data={"goldrows":goldrows,
                                      "goldcolumns":goldcolumns
                                      }, code="0", msg="成功")
        except Exception as e:
            return JsonResponse(msg="失败", code="999991", exception=e)
