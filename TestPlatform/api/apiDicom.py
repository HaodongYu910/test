from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Sum, Min

from rest_framework.authentication import TokenAuthentication
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
import threading

from ..common.api_response import JsonResponse
from ..models import stress, dicom, base_data, pid, GlobalHost, dicom_record, duration_record
from ..serializers import stress_Deserializer, \
    dicomdata_Deserializer, duration_Deserializer
from ..tools.smoke.gold import *
from ..tools.orthanc.deletepatients import *
from ..tools.dicom.dicomdetail import listUrl
from ..tools.stress.stress import updateStressData
from ..tools.stress.PerformanceResult import *
from ..tools.dicom.dicomdetail import *

logger = logging.getLogger(__name__)  # 这里使用 __name__ 动态搜索定义的 logger 配置


class dicomDetail(APIView):
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
            if not data["server"]:
                return JsonResponse(code="999996", msg="参数有误,必传参数 diseases, server！")

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
            server = data['server']
            try:
                if data['ids']:
                    dicomdata = dicom.objects.filter(vote=None, id__in=data['ids'])
                elif data['diseases']:
                    dicomdata = dicom.objects.filter(vote=None, diseases=data['diseases'])
                else:
                    dicomdata = dicom.objects.filter(vote=None)
                for i in dicomdata:
                    try:
                        i.vote, i.imagecount, i.slicenumber = voteData(i.studyinstanceuid, server, i.diseases)
                        i.save()
                    except Exception as e:
                        continue

            except ObjectDoesNotExist:
                return JsonResponse(code="999994", msg="数据未预测，请先预测！")
            return JsonResponse(code="0", msg="成功")
        except ObjectDoesNotExist:
            return JsonResponse(code="999995", msg="数据不存在！")


class dicomData(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def get(self, request):
        """
        获取dicom数据列表
        :param request:
        :return:
        """
        try:
            page_size = int(request.GET.get("page_size", 20))
            page = int(request.GET.get("page", 1))
        except (TypeError, ValueError):
            return JsonResponse(code="999985", msg="page and page_size must be integer!")
        diseases = request.GET.get("diseases")
        server = request.GET.get("server")
        slicenumber = request.GET.get("slicenumber")
        type = request.GET.get("type")
        if diseases is not None and server is None and slicenumber is None:
            obi = dicom.objects.filter(diseases__contains=diseases, type=type).order_by("-id")
        elif server is not None and diseases is None and slicenumber is None:
            obi = dicom.objects.filter(server__contains=server, type=type).order_by("-id")
        elif server is not None and diseases is not None and slicenumber is None:
            obi = dicom.objects.filter(server__contains=server, type=type, diseases__contains=diseases).order_by("-id")
        elif slicenumber is not None and server is None:
            obi = dicom.objects.filter(slicenumber__contains=slicenumber, type=type).order_by("-id")
        elif slicenumber is not None and server is not None:
            obi = dicom.objects.filter(server__contains=server, type=type, slicenumber__contains=slicenumber).order_by(
                "-id")
        elif type is not None:
            obi = dicom.objects.filter(type=type).order_by("-id")
        else:
            obi = dicom.objects.all().order_by("-id")
        paginator = Paginator(obi, page_size)  # paginator对象
        total = paginator.num_pages  # 总页数
        try:
            obm = paginator.page(page)
        except PageNotAnInteger:
            obm = paginator.page(1)
        except EmptyPage:
            obm = paginator.page(paginator.num_pages)
        serialize = dicomdata_Deserializer(obm, many=True)
        return JsonResponse(data={"data": serialize.data,
                                  "page": page,
                                  "total": total
                                  }, code="0", msg="成功")


class adddicomdata(APIView):
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
            if not data["server"] or not data["diseases"]:
                return JsonResponse(code="999996", msg="参数有误,必传参数 diseases, server！")

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
            server = data['server']
            if data['studyinstanceuid'] is None:
                StudyUID = connect_to_postgres(server,
                                               "select \"StudyInstanceUID\" from \"Study\" where \"PatientID\" ='{0}'".format(
                                                   data['patientid'])).to_dict(orient='records')
                if len(StudyUID) > 1:
                    return JsonResponse(code="999994", msg="数据重复！")
                else:
                    data['studyinstanceuid'] = StudyUID[0]['StudyInstanceUID']
            else:
                patientid = connect_to_postgres(server,
                                                "select \"PatientID\" from \"Study\" where \"StudyInstanceUID\" ='{0}'".format(
                                                    data['studyinstanceuid'])).to_dict(orient='records')
                data['patientid'] = patientid[0]['PatientID']
            try:
                data['vote'], SeriesInstanceUID = updateStressData(data['studyinstanceuid'], server)
            except ObjectDoesNotExist:
                return JsonResponse(code="999994", msg="数据未预测，请先预测！")

            dicomdata = dicomdata_Deserializer(data=data)

            with transaction.atomic():
                dicomdata.is_valid()
                dicomdata.save()
            return JsonResponse(code="0", msg="成功")
        except ObjectDoesNotExist:
            return JsonResponse(code="999995", msg="数据不存在！")


# 修改duration
class dicomUpdate(APIView):
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
            if not data["id"]:
                return JsonResponse(code="999996", msg="参数有误,必传参数 id！")

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
            obj = dicom.objects.get(id=data["id"])
            serializer = dicomdata_Deserializer(data=data)
            with transaction.atomic():
                if serializer.is_valid():
                    # 修改数据
                    serializer.update(instance=obj, validated_data=data)
                return JsonResponse(code="0", msg="成功")
        except ObjectDoesNotExist:
            return JsonResponse(code="999995", msg="数据不存在！")


# 删除dicom 数据
class deldicomdata(APIView):
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
        删除
        :param request:
        :return:
        """
        data = JSONParser().parse(request)
        result = self.parameter_check(data)
        if result:
            return result
        try:
            for j in data["ids"]:
                obj = dicom.objects.filter(id=j)
                obj.delete()
            return JsonResponse(code="0", msg="成功")
        except ObjectDoesNotExist:
            return JsonResponse(code="999995", msg="数据不存在！")


class dicomSend(APIView):
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
            # 必传参数  server_ip
            if not data["server"]:
                return JsonResponse(code="999996", msg="参数有误,必传参数 server_ip！")

        except KeyError:
            return JsonResponse(code="999996", msg="参数有误！")

    def post(self, request):
        """
        删除
        :param request:
        :return:
        """
        data = JSONParser().parse(request)
        result = self.parameter_check(data)
        if result:
            return result
        try:
            host = GlobalHost.objects.get(id=data["server"])
            if data['ids']:
                obj = base_data.objects.filter(id__in=data['ids'])
                for i in obj:
                    dicomobj = dicom.objects.filter(fileid=i.id)
                    for j in dicomobj:
                        delete_patients_duration(j.studyinstanceuid, data["server"], "StudyInstanceUID",False)
                    thread_Send = threading.Thread(target=Send, args=(host.host, i.content))
                    # 启动线程
                    thread_Send.start()
            else:
                obj = dicom.objects.filter(id__in=data['id'])
                for i in obj:
                    thread_Send = threading.Thread(target=Send, args=(data["server_ip"], i.route))
                    # 启动线程
                    thread_Send.start()

            return JsonResponse(code="0", msg="成功")
        except ObjectDoesNotExist:
            return JsonResponse(code="999995", msg="数据不存在！")


class dicomcsv(APIView):
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
        删除
        :param request:
        :return:
        """
        data = JSONParser().parse(request)
        result = self.parameter_check(data)
        if result:
            return result
        try:
            dicomsavecsv(data["ids"])
            return JsonResponse(code="0", msg="成功")
        except ObjectDoesNotExist:
            return JsonResponse(code="999995", msg="数据不存在！")


class deldicomResult(APIView):
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
        删除
        :param request:
        :return:
        """
        data = JSONParser().parse(request)
        result = self.parameter_check(data)
        if result:
            return result
        try:
            delreport(data['server'], data["ids"])
            return JsonResponse(code="0", msg="执行成功")
        except ObjectDoesNotExist:
            return JsonResponse(code="999995", msg="数据不存在！")


class Update_base_Data(APIView):
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
            # 必传参数 content, status , type
            if not data["content"] or not data["type"] or not data["status"]:
                return JsonResponse(code="999996", msg="参数有误！")

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
            obj = stress.objects.get(id=data["id"])
        except ObjectDoesNotExist:
            return JsonResponse(code="999995", msg="数据不存在！")
        # 查找是否相同名称
        pro_name = stress.objects.filter(content=data["content"]).exclude(id=data["id"])
        if len(pro_name):
            return JsonResponse(code="999997", msg="存在相同内容数据")
        else:
            serializer = stress_Deserializer(data=data)
            with transaction.atomic():
                if serializer.is_valid():
                    # 修改数据
                    serializer.update(instance=obj, validated_data=data)
                    return JsonResponse(code="0", msg="成功")
                else:
                    return JsonResponse(code="999998", msg="失败")


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
            # 环境 类型 online，Autotest
            if data["service"] not in ["staging", "Autotest"]:
                return JsonResponse(code="999996", msg="service参数有误！staging，Autotest")

        except KeyError:
            return JsonResponse(code="999996", msg="参数有误！")


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
            # 环境 类型 online，Autotest
            if data["service"] not in ["staging", "Autotest"]:
                return JsonResponse(code="999996", msg="service参数有误！staging，Autotest")

        except KeyError:
            return JsonResponse(code="999996", msg="参数有误！")


class dicomUrl(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def parameter_check(self, data):
        """
        校验参数
        :param data:
        :return:
        """
        try:
            # 必传参数 type
            if not data["type"]:
                return JsonResponse(code="999996", msg="参数有误,必传参数 type, id！")

        except KeyError:
            return JsonResponse(code="999996", msg="参数有误！")

    def post(self, request):
        """
        返回url
        :param request:
        :return:
        """
        data = JSONParser().parse(request)
        result = self.parameter_check(data)
        if result:
            return result
        try:
            type = data['type']
            try:
                if type == 'gold':
                    obj = dicom_record.objects.get(id=data['id'])
                    kc, url = listUrl(obj.hostid, obj.studyinstanceuid)
                elif type == 'duration':
                    obj = duration_record.objects.get(id=data['id'])
                    kc, url = listUrl(obj.hostid, obj.studyinstanceuid)
                else:
                    dicomdata = dicom.objects.filter(vote=None)
            except ObjectDoesNotExist:
                return JsonResponse(code="999994", msg="数据未预测，请先预测！")
            return JsonResponse(code="0", msg="成功", data={
                "url": url,
                "kc": kc
            })
        except ObjectDoesNotExist:
            return JsonResponse(code="999995", msg="数据不存在！")
