from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Sum,Min

from rest_framework.authentication import TokenAuthentication
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
import shutil

from TestPlatform.common.api_response import JsonResponse
from TestPlatform.models import  base_data, pid, GlobalHost
from TestPlatform.serializers import duration_Deserializer
from ..tools.orthanc.deletepatients import *
from ..tools.dicom.duration_verify import *
from ..tools.stress.PerformanceResult import *

logger = logging.getLogger(__name__)  # 这里使用 __name__ 动态搜索定义的 logger 配置


# 获取 持续化数据
class getDuration(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def get(self, request):
        """
        获取持续话记录
        :param request:
        :return:
        """
        obi = duration.objects.filter().order_by("server")
        durationdata = duration_Serializer(obi, many=True)
        du = durationdata.data
        for i in du:
            obj = duration_record.objects.filter(duration_id=i["id"],
                                                 create_time__gte=i["update_time"])
            i['send'] = str(obj.count())

        return JsonResponse(data={"data": durationdata.data
                                  }, code="0", msg="成功")


# 获取 持续化发送详细数据
class durationData(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def get(self, request):
        """
        获取持续列表详细数据
        :param request:
        :return:
        """
        try:
            page_size = int(request.GET.get("page_size", 20))
            page = int(request.GET.get("page", 1))
        except (TypeError, ValueError):
            return JsonResponse(code="999985", msg="page and page_size must be integer!")
        type = request.GET.get("type")
        durationid = int(request.GET.get("id"))
        datalist = {}

        # 判断是否有查询时间
        if request.GET.get("startdate"):
            startdate = request.GET.get("startdate")
        else:
            startdate = '2000-01-01 00:00:00'

        if request.GET.get("enddate"):
            enddate = request.GET.get("enddate")
        else:
            enddate = datetime.datetime.now()

        # 判断查询数据类型
        if type == 'patientid':
            patientid = request.GET.get("patientid")
            obi = duration_record.objects.filter(duration_id=durationid, patientid__contains=patientid).order_by("-id")
        elif type == 'Not_sent':
            obi = duration_record.objects.filter(duration_id=durationid, aistatus__isnull=True,
                                                 create_time__lte=enddate, create_time__gte=startdate).order_by("-id")
        elif type == 'sent':
            obi = duration_record.objects.filter(duration_id=durationid, aistatus__isnull=False,
                                                 create_time__lte=enddate, create_time__gte=startdate).order_by("-id")
        elif type == 'AiTrue':
            obi = duration_record.objects.filter(duration_id=durationid, aistatus__in=[1, 2], create_time__lte=enddate,
                                                 create_time__gte=startdate).order_by("-id")
        elif type == 'AiFalse':
            obi = duration_record.objects.filter(duration_id=durationid, aistatus__in=[-1, -2, 3],
                                                 create_time__lte=enddate, create_time__gte=startdate).order_by("-id")
        else:
            obi = duration_record.objects.filter(duration_id=durationid, create_time__lte=enddate,
                                                 create_time__gte=startdate).order_by("-id")
        paginator = Paginator(obi, page_size)  # paginator对象
        total = paginator.num_pages  # 总页数
        count = paginator.count  # 总页数
        try:
            obm = paginator.page(page)
        except PageNotAnInteger:
            obm = paginator.page(1)
        except EmptyPage:
            obm = paginator.page(paginator.num_pages)
        serialize = duration_record_Deserializer(obm, many=True)
        rdata = serialize.data
        du = duration.objects.get(id=durationid)
        if du.dds is not None:
            server = du.dds
        else:
            server = du.server
        try:
            datalist['sent'] = durationtotal(obi, server, '1,2')
            datalist['ai_false'] = durationtotal(obi, server, '-2,-1,1,2,3')
            datalist['ai_true'] = durationtotal(obi, server, '1,2')
            datalist['ai_false'] = durationtotal(obi, server, '-2,3')
            datalist['notai'] = durationtotal(obi, server, '-1')
            datalist['all'] = obi.count()
            datalist['notsent'] = int(datalist['all']) - int(datalist['sent'])
        except ValueError:
            return JsonResponse(data={"data": datalist
                                      }, code="0", msg="测试环境数据库连接失败")
        for i in rdata:
            try:
                dbresult = connect_to_postgres(server,
                                               "SELECT aistatus,diagnosis,imagecount,insertiontime FROM study_view WHERE studyinstanceuid =\'{0}\'".format(
                                                   i["studyinstanceuid"]))
                _dict = dbresult.to_dict(orient='records')
            except Exception as e:
                logger.error(e)
            if _dict == []:
                i['aistatus'] = None
                i['diagnosis'] = None
                i['imagecount_server'] = None
            else:
                for j in _dict:
                    i['aistatus'] = j['aistatus']
                    i['diagnosis'] = j['diagnosis']
                    i['imagecount_server'] = j['imagecount']

        return JsonResponse(data={"data": rdata,
                                  "durationresult": [datalist],
                                  "page": page,
                                  "total": total,
                                  "count": count
                                  }, code="0", msg="成功")


# 保存dicom 发送记录
class add_duration(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def parameter_check(self, data):
        """
        校验参数
        :param data:
        :return:
        """
        try:
            # 必传参数 key, server_ip , type
            if not data["duration"] or not data["server"]:
                return JsonResponse(code="999996", msg="参数有误,必传参数 duration, server！")

        except KeyError:
            return JsonResponse(code="999996", msg="参数有误！")

    def post(self, request):
        """
        send数据
        :param request:
        :return:
        """
        data = JSONParser().parse(request)
        result = self.parameter_check(data)
        if result:
            return result
        try:
            if data['series'] is True:
                data['series'] = '1'
            else:
                data['series'] = '0'
            data['duration'] = ','.join(data['duration'])
            obj = GlobalHost.objects.get(host=str(data['server']))
            data['aet'] = obj.description
            duration = duration_Deserializer(data=data)

            with transaction.atomic():
                duration.is_valid()
                duration.save()
            return JsonResponse(code="0", msg="成功")
        except ObjectDoesNotExist:
            return JsonResponse(code="999995", msg="数据不存在！")


# 修改duration
class update_duration(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def parameter_check(self, data):
        """
        校验参数
        :param data:
        :return:
        """
        try:
            # 必传参数 key, server_ip , type
            if not data["duration"]:
                return JsonResponse(code="999996", msg="参数有误,必传参数 duration！")

        except KeyError:
            return JsonResponse(code="999996", msg="参数有误！")

    def post(self, request):
        """
        send数据
        :param request:
        :return:
        """
        data = JSONParser().parse(request)
        result = self.parameter_check(data)
        if result:
            return result
        try:
            if data['series'] is True:
                data['series'] = '1'
            else:
                data['series'] = '0'
            obj = duration.objects.get(id=data["id"])
            data['duration'] = ','.join(data['duration'])
            keyword = duration.objects.filter(keyword=data["keyword"])
            if len(keyword):
                return JsonResponse(code="999997", msg="存在相同匿名名称数据，请修改")
            else:
                serializer = duration_Deserializer(data=data)
                with transaction.atomic():
                    if serializer.is_valid():
                        # 修改数据
                        serializer.update(instance=obj, validated_data=data)
                return JsonResponse(code="0", msg="成功")
        except ObjectDoesNotExist:
            return JsonResponse(code="999995", msg="数据不存在！")


class DisableDuration(APIView):
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
        禁用dicom 发送
        :param request:
        :return:
        """
        data = JSONParser().parse(request)
        result = self.parameter_check(data)
        if result:
            return result
        try:
            # 查找pid
            obj = pid.objects.filter(durationid=data["id"])
            okj = duration.objects.get(id=data["id"])
            folder_fake = "{0}/{1}".format('/files/logs', str(okj.keyword))
            for i in obj:
                cmd = 'kill -9 {0}'.format(int(i.pid))
                logger.info(cmd)
                os.system(cmd)
                i.delete()
                time.sleep(1)
            if os.path.exists(folder_fake):
                shutil.rmtree(folder_fake)
            okj.sendstatus = False
            okj.save()

            return JsonResponse(code="0", msg="成功")
        except ObjectDoesNotExist:
            return JsonResponse(code="999995", msg="无法正常关闭！")


class EnableDuration(APIView):
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
            if not isinstance(data["id"], int):
                return JsonResponse(code="999996", msg="参数有误！")
        except KeyError:
            return JsonResponse(code="999996", msg="参数有误！")

    def post(self, request):
        """
        启用dicom 发送
        :param request:
        :return:
        """
        data = JSONParser().parse(request)
        result = self.parameter_check(data)
        if result:
            return result
        # 查找id是否存在
        try:
            durationid = data["id"]
            obj = duration.objects.get(id=durationid)
            sleepcount=  obj.sleepcount if obj.sleepcount is not None else 9999
            sleeptime = obj.sleeptime if obj.sleeptime is not None else 0

            if obj.sendcount is None and obj.end is None:
                start = 0
                end = 1
            elif obj.sendcount is None and obj.end is not None:
                start = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                end = (datetime.datetime.now() + datetime.timedelta(hours=int(obj.end))).strftime(
                    "%Y-%m-%d %H:%M:%S")
            else:
                start = 0
                min = 10000
                sumdicom = 0
                for j in obj.dicom.split(","):
                    dicom = base_data.objects.get(remarks=j)
                    if dicom.other is None:
                        sumdicom = sumdicom
                    else:
                        if min > int(dicom.other):
                            min = int(dicom.other)
                        sumdicom = int(dicom.other) + sumdicom

            for i in obj.dicom.split(","):
                dicom = base_data.objects.get(remarks=i)
                folder = dicom.content
                if sumdicom:
                    imod = divmod(int(obj.sendcount), sumdicom)
                    imin = divmod(int(imod[1]), min)
                    if int(imin[1]) < (int(imin[1]) / 2):
                        mincount = int(imin[0]) + int(imod[0])
                    else:
                        mincount = int(imin[0]) + int(imod[0]) + 1
                    end = mincount if int(dicom.other) == int(min) else imod[0]

                cmd = ('nohup /home/biomind/.local/share/virtualenvs/biomind-dvb8lGiB/bin/python3'
                       ' /home/biomind/Biomind_Test_Platform/TestPlatform/tools/duration/dicomSend.py '
                       '--ip {0} --aet {1} '
                       '--port {2} '
                       '--keyword {3} '
                       '--dicomfolder {4} '
                       '--durationid {5} '
                       '--diseases {6} '
                       '--start {7} '
                       '--end {8} &').format(obj.server, obj.aet, obj.port, obj.keyword, folder, durationid, i,
                                             start, end, sleepcount, sleeptime, obj.series)

                       # '--sleepcount {9} '
                       # '--sleeptime {10} '
                       # '--series {11} &'
                logger.info(cmd)
                os.system(cmd)
                time.sleep(1)

            obj.sendstatus = True
            obj.save()
            return JsonResponse(code="0", msg="成功")
        except ObjectDoesNotExist:
            return JsonResponse(code="999995", msg="运行失败！")


# 删除dicom 发送记录
class del_duration(APIView):
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
        删除项目
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
                    obj = duration.objects.get(id=i)
                    try:
                        obj.delete()
                    except ObjectDoesNotExist:
                        return JsonResponse(code="999994", msg="删除失败！")
                    return JsonResponse(code="0", msg="成功")
                except ObjectDoesNotExist:
                    return JsonResponse(code="999995", msg="数据不存在！")

        except ObjectDoesNotExist:
            return JsonResponse(code="999995", msg="执行失败！")


# 删除dicom 数据
class delete_patients(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def parameter_check(self, data):
        """
        校验参数
        :param data:
        :return:
        """
        try:
            # 必传参数 key, server_ip , type
            if not data["testtype"] or not data["server_ip"]:
                return JsonResponse(code="999996", msg="参数有误,必传参数 key, server_ip！")

        except KeyError:
            return JsonResponse(code="999996", msg="参数有误！")

    def post(self, request):
        """
        删除数据
        :param request:
        :return:
        """
        data = JSONParser().parse(request)
        result = self.parameter_check(data)
        if result:
            return result
        #
        try:
            delete_patients_duration(data['deldata'], data['server_ip'], data['testtype'], data['fuzzy'])
            return JsonResponse(code="0", msg="成功")
        except ObjectDoesNotExist:
            return JsonResponse(code="999995", msg="数据不存在！")



class duration_verify(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def get(self, request):
        """
        更新持续化记录
        :param request:
        :return:
        """
        id = request.GET.get("id")
        data = verifyData(id)
        return JsonResponse(data={"data": data
                                  }, code="0", msg="成功")
