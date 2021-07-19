from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db import transaction
from django.conf import settings
from rest_framework.authentication import TokenAuthentication
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
import threading
import datetime
import shutil

from influxdb import InfluxDBClient
from ..common.getdicom import *
from ..models import duration, dicom_relation, dicom
from ..serializers import duration_Deserializer, duration_Serializer, duration_record_Deserializer, \
    dicomdata_Deserializer
from ..common.anonymization import onlyDoAnonymization
from ..common.dds_detect import *
from ..common.deletepatients import *
from AutoDicom.common.dicomBase import baseTransform
from ..common.durationSend import DurationThread

from AutoProject.scheduletask import DurationSyTask
from AutoProject.common.api_response import JsonResponse
from AutoProject.models import project_version
from ..common.duration import durationSend,NormalSend

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
        try:
            Host = request.GET.get("server")
            if int(request.GET.get("type")) in [0, 1]:
                durationType = [0, 1]
            else:
                durationType = [2, 3]

            page_size = int(request.GET.get("page_size", 10))
            page = int(request.GET.get("page", 1))
            project_id = request.GET.get("project_id")
        except (TypeError, ValueError):
            return JsonResponse(code="999985", msg="page and page_size must be integer!")
        if Host:
            obi = duration.objects.filter(project_id=project_id, Host=Host, type__in=durationType).order_by(
                "-sendstatus")

        else:
            obi = duration.objects.filter(project_id=project_id, type__in=durationType).order_by("-id").order_by(
                "-sendstatus")

        paginator = Paginator(obi, page_size)  # paginator对象
        total = paginator.num_pages  # 总页数
        try:
            obm = paginator.page(page)
        except PageNotAnInteger:
            obm = paginator.page(1)
        except EmptyPage:
            obm = paginator.page(paginator.num_pages)
        dataSerializer = duration_Serializer(obm, many=True)
        for i in dataSerializer.data:
            # 已发送的数据统计
            i['send'] = duration_record.objects.filter(relation_id=i["id"], create_time__gte=i["update_time"]).count()
            i['totalsend'] = duration_record.objects.filter(relation_id=i["id"]).count()
            i['todaysend'] = duration_record.objects.filter(relation_id=i["id"], create_time__gte=datetime.datetime.now().strftime("%Y-%m-%d 00:00:00")).count()
            if i['version'] is not None:
                i['version'] = project_version.objects.get(id=i['version']).version
            i["dicomLabel"] = baseTransform(i["dicom"], 'base')

        return JsonResponse(data={"data": dataSerializer.data,
                                  "page": page,
                                  "total": total
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
        relation_id = int(request.GET.get("id"))
        patientname = request.GET.get("patientname")

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
        if patientname:
            obi = duration_record.objects.filter(relation_id=relation_id, patientname__contains=patientname).order_by(
                "-id")
        elif type == 'Not_sent':
            obi = duration_record.objects.filter(relation_id=relation_id, aistatus__isnull=True,
                                                 create_time__lte=enddate, create_time__gte=startdate).order_by("-id")
        elif type == 'sent':
            obi = duration_record.objects.filter(relation_id=relation_id, aistatus__isnull=False,
                                                 create_time__lte=enddate, create_time__gte=startdate).order_by("-id")
        elif type == 'AiTrue':
            obi = duration_record.objects.filter(relation_id=relation_id, aistatus__in=[3, 2], create_time__lte=enddate,
                                                 create_time__gte=startdate).order_by("-id")
        elif type == 'AiFalse':
            obi = duration_record.objects.filter(relation_id=relation_id, aistatus__in=[-1, -2, 1],
                                                 create_time__lte=enddate, create_time__gte=startdate).order_by("-id")
        else:
            obi = duration_record.objects.filter(relation_id=relation_id, create_time__lte=enddate,
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
        serialize = duration_record_Deserializer(obm, many=True)  # obi是从数据库取出来的全部数据，obm是数据库取出来的数据分页之后的数据

        client = InfluxDBClient(host='192.168.1.121', port=8086, database='auto_test')
        for i in serialize.data:
            try:
                result = client.query(
                    f'select count(value),MEAN(value) from duration where id=\'{i["relation_id"]}\' and studyuid=\'{i["studyinstanceuid"]}\';')
                i["time"] = list(result)[0][0]['mean']
                i["imagecount"] = list(result)[0][0]['count']
            except:
                i["time"] = 0
                i["imagecount"] = 0
                continue

        return JsonResponse(data={"data": serialize.data,
                                  "page": page,
                                  "total": total,
                                  "count": count
                                  }, code="0", msg="成功")


class getdurationsource(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def get(self, request):
        """
        获取持续数据源信息
        :param request:
        :return:
        """
        try:
            relation_id = int(request.GET.get("id"))
        except (TypeError, ValueError):
            return JsonResponse(code="999985", msg="relation_id must be integer!")

        try:
            obj = duration_record.objects.get(id=relation_id)
            dicomObj = dicom.objects.get(studyinstanceuid=obj.studyolduid)

        except (TypeError, ValueError):
            return JsonResponse(code="999985", msg="无此数据!")

        try:
            oldPath = dicom_relation.objects.get(success_uid=dicomObj.studyinstanceuid).old_path
        except Exception as e:
            logger.error(e)
            oldPath = ''
        data = {
            "patientid": dicomObj.patientid,
            "patientname": dicomObj.patientname,
            "studyinstanceuid": dicomObj.studyinstanceuid,
            "diseases": dicomObj.diseases,
            "imagecount": dicomObj.imagecount,
            "route": dicomObj.route,
            "status": dicomObj.status,
            "oldPath": oldPath
        }
        return JsonResponse(data=data, code="0", msg="成功")


class addDuration(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def parameter_check(self, data):
        """
        校验参数
        :param data:
        :return:
        """
        try:
            # 必传参数 dicom, Host
            if not data["dicom"] or not data["Host"]:
                return JsonResponse(code="999996", msg="参数有误,必传参数 duration, server！")

        except KeyError:
            return JsonResponse(code="999996", msg="参数有误,必传参数 dicom, server！")

    def post(self, request):
        """
        添加发送数据
        :param request:
        :return:
        """
        data = JSONParser().parse(request)
        result = self.parameter_check(data)
        group = ""
        dicom = ""
        if result:
            return result
        try:
            dicomdata = ''
            hostobj = Server.objects.get(id=data['Host'])
            data['server'] = hostobj.host

            # data['dicom'] = ','.join(data['dicom'])
            for i in data['dicom']:
                if i[0] == "虚拟组":
                    group = group + "{},".format(i[1])
                else:
                    dicomdata = dicomdata + "{},".format(str(i[1]))

            data['dicom'] = dicomdata[:-1]
            data['group'] = group[:-1]
            data['aet'] = hostobj.remarks
            duration = duration_Deserializer(data=data)

            with transaction.atomic():
                duration.is_valid()
                duration.save()
            return JsonResponse(code="0", msg="成功")
        except Exception as e:
            return JsonResponse(code="999995", msg="添加失败:{}！".format(e))


class updateDuration(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def parameter_check(self, data):
        """
        校验参数
        :param data:
        :return:
        """
        try:
            # 必传参数 dicom
            if not data["id"]:
                return JsonResponse(code="999996", msg="参数有误,必传参数 dicom！")

        except KeyError:
            return JsonResponse(code="999996", msg="参数有误！")

    def post(self, request):
        """
        修改持续化数据
        :param request:
        :return:
        """
        data = JSONParser().parse(request)
        result = self.parameter_check(data)
        if result:
            return result
        try:
            obj = duration.objects.get(id=data["id"])
            dicomdata = ""
            group = ""
            for i in data['dicom']:
                if i[0] == "虚拟组":
                    group = group + "{},".format(i[1])
                else:
                    dicomdata = dicomdata + "{},".format(str(i[1]))

            data['dicom'] = dicomdata[:-1]
            data['group'] = group[:-1]
            # 修改数据
            serializer = duration_Deserializer(data=data)
            with transaction.atomic():
                if serializer.is_valid():
                    serializer.update(instance=obj, validated_data=data)
                    return JsonResponse(code="0", msg="成功")
                else:
                    return JsonResponse(code="999995", msg="修改失败！")
        except ObjectDoesNotExist:
            return JsonResponse(code="999995", msg="修改失败！")


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
            obj = duration.objects.get(id=data["id"])
            if obj.type ==2:
                full_fn_fake = f'/lfs/QA/durationlogs/Duration{obj.id}'
            else:
                full_fn_fake = f'{settings.LOG_PATH}/{obj.type}{obj.id}'
            shutil.rmtree(full_fn_fake)
            obj.sendstatus = False
            obj.save()

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
        启用 dicom 发送
        :param request:
        :return:
        """
        data = JSONParser().parse(request)
        result = self.parameter_check(data)
        if result:
            return result
        # 查找id是否存在
        try:
            obj = duration.objects.get(id=data["id"])
            obj.start_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            SendStatus = True
            if obj.type == 1:
                SendStatus = durationSend(data["id"])
                # durationThread = DurationThread(id=data["id"])
                # durationThread.setDaemon(True)
                # # 开始线程
                # durationThread.start()
            elif obj.type == 0:
                SendStatus = NormalSend(data["id"])
            else:
                cmd = f"nohup /home/biomind/.local/share/virtualenvs/biomind-dvb8lGiB/bin/python3 /home/biomind/Biomind_Test_Platform/AutoDicom/common/durationTask.py --relation_id {obj.id} &"
                logger.info(cmd)
                os.system(cmd)

            if SendStatus is True:
                obj.status = True
                obj.save()
                return JsonResponse(code="0", msg="成功")
            else:
                return JsonResponse(code="999995", msg="运行失败！")
        except ObjectDoesNotExist:
            return JsonResponse(code="999995", msg="运行失败！")


class delDuration(APIView):
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
        删除dicom 发送记录
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
                    duration.objects.get(id=i).delete()
                    try:
                        duration_record.objects.filter(relation_id=i).delete()
                    except ObjectDoesNotExist:
                        return JsonResponse(code="999994", msg="删除失败！")
                except ObjectDoesNotExist:
                    return JsonResponse(code="999995", msg="数据不存在！")
            return JsonResponse(code="0", msg="成功")
        except ObjectDoesNotExist:
            return JsonResponse(code="999995", msg="删除失败！")


# 删除dicom 数据
class deletePatients(APIView):
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
            data = delete_patients_duration(data['deldata'], data['serverID'], data['testtype'], data['fuzzy'])
            return JsonResponse(code="0", msg="成功", data=data)
        except ObjectDoesNotExist:
            return JsonResponse(code="999995", msg="数据不存在！")


class anonymizationAPI_2nd(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    # 判断是否需要匿名化或者存储这个匿名后的数据到一个新的folder？
    def post(self, request):
        data = JSONParser().parse(request)  # 将传入的json数据转换为可识别的内容
        try:
            name = data['anon_name']
            # addr = 'C:\\Users\\yuhaodong\\Desktop\\train'
            addr = data['anon_addr']
            disease = data['anon_disease']
            wPN = data['wPN']
            wPID = data['wPID']
            ap_addr = data['appointed_addr']  # appointed storage address

            # 将匿名化后的数据入库
            # 调用后端服务，对传入的文件夹进行匿名化
            t = threading.Thread(target=onlyDoAnonymization(addr, {"No": 0}, disease, wPN, wPID, name, ap_addr))
            t.start()
            return JsonResponse(code="0", msg="匿名化开始")
        except ObjectDoesNotExist:
            return JsonResponse(code="999995", msg="出问题了....")


class get_dicomAPI_2nd(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    # 发送post请求
    def post(self, request):
        data = JSONParser().parse(request)  # 将传入的json数据转换为可识别的内容
        try:
            PID = data['PID']  # 待查询数据的patientname
            # addr = 'C:\\Users\\yuhaodong\\Desktop\\train'
            destIP = data['destIP']  # 发送目标服务器ip
            destUSR = data['destUSR']  # 发送目标服务器用户名
            destPSW = data['destPSW']  # 发送目标服务器密码
            if destIP and destPSW and destPSW:
                t = threading.Thread(target=getDicomServe(PID, destIP, destUSR, destPSW))
                t.start()
                data['url'] = ""
                return JsonResponse(code="0", msg="开始提取数据至服务器", data=data)
            else:
                url = get_to_local(PID)
                data['url'] = url
                return JsonResponse(code="0", msg="开始提取数据至本地", data=data)
        except ObjectDoesNotExist:
            return JsonResponse(code="999995", msg="出问题了....")


class ddsDataVerifyAPI(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def post(self, request):
        data = JSONParser().parse(request)
        try:
            ip = data['search_target_ip']
            time = data['search_duration']
            id = data['id']

            t = threading.Thread(target=dataVerify(ip, id))
            t.start()
            return JsonResponse(code="0", msg="开始搜索")
        except ObjectDoesNotExist:
            return JsonResponse(code="999995", msg="出问题了....")


class getDurationTB(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def get(self, request):
        """
        获取持续化同步结构
        :param request:
        :return:
        """
        try:
            DurationSyTask()
        except (TypeError, ValueError):
            return JsonResponse(code="999985", msg="page and page_size must be integer!")
        return JsonResponse(code="0", msg="成功")
