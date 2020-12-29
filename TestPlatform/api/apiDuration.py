from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Avg

from rest_framework.authentication import TokenAuthentication
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
import shutil,threading

from TestPlatform.common.api_response import JsonResponse
from TestPlatform.models import base_data, pid, GlobalHost
from TestPlatform.serializers import duration_Deserializer
from ..tools.dicom.anonymization import onlyDoAnonymization
from ..tools.orthanc.deletepatients import *
from ..tools.dicom.duration_verify import *
from ..tools.stress.PerformanceResult import *
from ..common.dicom import anonymousSend
from ..common.duration import verifyDuration,durationtotal

logger = logging.getLogger(__name__)  # 这里使用 __name__ 动态搜索定义的 logger 配置


# 获取 持续化数据列表
class getDuration(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def get(self, request):
        """
        获取持续话记录
        :param request:
        :return:
        """
        # ','.join(data['dicom'])
        obi = duration.objects.filter().order_by("server")
        dataSerializer = duration_Serializer(obi, many=True)

        for i in dataSerializer.data:
            dicomdata = ''
            # 已发送的数据统计
            obj = duration_record.objects.filter(duration_id=i["id"],create_time__gte = i["update_time"])
            i['send'] = str(obj.count())
            # dicom id 转换成病种文案
            for j in i["dicom"].split(","):
                try:
                    obj = base_data.objects.get(id=j)
                    name = obj.remarks
                except Exception as e:
                    logger.error("id:{0}文件已经删除了".format(j))
                    name ="Null"
                dicomdata = dicomdata + name +","
            i["dicom"] = dicomdata

        return JsonResponse(data={"data": dataSerializer.data
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
        try:
            verifyDuration(durationid)
        except Exception as e:
            logger.error(e)
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
        serialize = duration_record_Deserializer(obm, many=True) # obi是从数据库取出来的全部数据，obm是数据库取出来的数据分页之后的数据
        durationData = serialize.data
        try:
            datalist = durationtotal(durationid)
            datalist['all'] = obi.count()
            datalist['sent'] = int(datalist['all']) - int(datalist['notsent'])
            avg = duration_record.objects.filter(duration_id=durationid).aggregate(Avg("time"))
            datalist['avg'] = 1/avg['time__avg']
        except ValueError:
            return JsonResponse(data={"data": datalist
                                      }, code="0", msg="测试环境数据库连接失败")

        return JsonResponse(data={"data": durationData,
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
            if not data["dicom"] or not data["hostid"]:
                return JsonResponse(code="999996", msg="参数有误,必传参数 duration, server！")

        except KeyError:
            return JsonResponse(code="999996", msg="参数有误,必传参数 dicom, server！")

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
            dicomdata = ''
            hostobj = GlobalHost.objects.get(id=data['hostid'])
            data['server']= hostobj.host
            # data['dicom'] = ','.join(data['dicom'])
            for i in data['dicom']:
                dicomdata = dicomdata + str(i[1]) + ','
            data['dicom'] = dicomdata[:-1]

            obj = GlobalHost.objects.get(host=str(data['server']))
            data['aet'] = obj.description
            duration = duration_Deserializer(data=data)

            with transaction.atomic():
                duration.is_valid()
                duration.save()
            return JsonResponse(code="0", msg="成功")
        except Exception as e:
            print(e)
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
            if not data["dicom"]:
                return JsonResponse(code="999996", msg="参数有误,必传参数 dicom！")

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
            dicomdata=''
            for i in data['dicom']:
                dicomdata = dicomdata + str(i[1]) + ','
            data['dicom'] = dicomdata[:-1]
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

            for i in obj:
                cmd = 'kill -9 {0}'.format(int(i.pid))
                logger.info(cmd)
                os.system(cmd)
                i.delete()

            okj.sendstatus = False
            okj.save()
            # 删除 文件夹
            folder="/files/logs/{0}".format(str(okj.keyword))
            if os.path.exists(folder):
                shutil.rmtree(folder)

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
            result=anonymousSend(data["id"], "type")
            if result is True:
                return JsonResponse(code="0", msg="成功")
            else:
                return JsonResponse(code="999995", msg="失败！")
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
            if not data["testtype"] or not data["serverID"]:
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
            delete_patients_duration(data['deldata'], data['serverID'], data['testtype'], data['fuzzy'])
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


class anonymizationAPI_2nd(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    # 判断是否需要匿名化或者存储这个匿名后的数据到一个新的folder？
    def post(self, request):
        data = JSONParser().parse(request)  # 将传入的json数据转换为可识别的内容
        try:
            name = data['anon_name']
            #addr = 'C:\\Users\\yuhaodong\\Desktop\\train'
            addr = data['anon_addr']
            disease = data['anon_disease']
            wPN = data['wPN']
            wPID = data['wPID']

            # 将匿名化后的数据入库
            # 调用后端服务，对传入的文件夹进行匿名化
            t = threading.Thread(target=onlyDoAnonymization(addr, {"No": 0}, disease, wPN, wPID, name))
            t.start()
            return JsonResponse(code="0", msg="匿名化开始")
        except ObjectDoesNotExist:
            return JsonResponse(code="999995", msg="出问题了....")

