from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from rest_framework.authentication import TokenAuthentication
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
import threading

from TestPlatform.common.api_response import JsonResponse
from TestPlatform.models import stress_record, stress_data,duration
from TestPlatform.serializers import stressrecord_Deserializer,\
    stress_data_Deserializer,duration_Deserializer,duration_Serializer
from ..common.stress import sequence
from ..tools.orthanc.delete_patients import *
from ..tools.duration_verify import *
from ..tools.dicom.duration import send_duration
from ..tools.stress.PerformanceResult import *

logger = logging.getLogger(__name__)  # 这里使用 __name__ 动态搜索定义的 logger 配置，这里有一个层次关系的知识点。


class stressversion(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def get(self, request):
        """
        获取压测记录
        :param request:
        :return:
        """
        list = []
        server=request.GET.get("server", '192.168.1.208')
        obi = stress_record.objects.filter(loadserver__contains=server).order_by("-id")
        serialize = stressrecord_Deserializer(obi, many=True)
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
        获取项目列表
        :param request:
        :return:
        """
        try:
            page_size = int(request.GET.get("page_size", 20))
            page = int(request.GET.get("page", 1))
        except (TypeError, ValueError):
            return JsonResponse(code="999985", msg="page and page_size must be integer!")
        diseases = request.GET.get("diseases")
        if diseases:
            obi = stress_data.objects.filter(diseases__contains=diseases).order_by("-id")
        else:
            obi = stress_data.objects.all().order_by("-id")
        paginator = Paginator(obi, page_size)  # paginator对象
        total = paginator.num_pages  # 总页数
        try:
            obm = paginator.page(page)
        except PageNotAnInteger:
            obm = paginator.page(1)
        except EmptyPage:
            obm = paginator.page(paginator.num_pages)
        serialize = stress_data_Deserializer(obm, many=True)
        return JsonResponse(data={"data": serialize.data,
                                  "page": page,
                                  "total": total
                                  }, code="0", msg="成功")

class stressResult(APIView):
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
            if not data["version"] or not data["checkversion"]:
                return JsonResponse(code="999996", msg="缺失必要参数,参数 version,checkversion！")

        except KeyError:
            return JsonResponse(code="999996", msg="参数有误！")

    def post(self, request):
        """
        预测时间 压测结果
        :param request:
        :return:
        """
        data = JSONParser().parse(request)
        result = self.parameter_check(data)
        if result:
            return result

        try:
            starttime = stress_record.objects.get(version=data['version']).start_date
            endtime = stress_record.objects.get(version=data['version']).end_date
            start_time = stress_record.objects.get(version=data['checkversion']).start_date
            end_time = stress_record.objects.get(version=data['checkversion']).end_date

            checkdate = [[starttime,endtime], [start_time,end_time]]
            predictionfield =['avg_pred_time', 'median_pred_time', 'min_pred_time', 'max_pred_time', 'coef']
            jobfield =['avg_job_time', 'avg_single_job_time', 'median_job_time', 'min_job_time', 'max_job_time',
                 'coef']
            predictionresult = datacheck('prediction', predictionfield, checkdate,data['server'])
            jobresult = datacheck('job', jobfield, checkdate,data['server'])
            # lungresult=lung('job', jobfield, checkdate,data['server'])
            return JsonResponse(data={"data": predictionresult,
                                      "jobresult":jobresult
                                      }, code="0", msg="成功")
        except Exception as e:
            return JsonResponse(msg="失败", code="999991", exception=e)

class stresstool(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def parameter_check(self, data):
        """
        验证参数
        :param data:
        :return:
        """
        try:
            # 必传参数 loadserver, testdata, loop_time
            if not data["loadserver"] or not data["testdata"] or not data["loop_time"]:
                return JsonResponse(code="999996", msg="缺失必要参数,参数 loadserver, testdata, loop_time！")

        except KeyError:
            return JsonResponse(code="999996", msg="参数有误！")

    def post(self, request):
        """
        执行压测脚本
        :param request:
        :return:
        """
        data = JSONParser().parse(request)
        result = self.parameter_check(data)
        if result:
            return result

        try:
            testdata=data['testdata']
            end_time = (datetime.datetime.now() + datetime.timedelta(hours=int(data["loop_time"]))).strftime("%Y-%m-%d %H:%M:%S")
            data['testdata'] = str(data["testdata"])
            data['start_date'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            data['end_date'] = end_time

            # 查找是否相同版本号的测试记录
            stress_version = stress_record.objects.filter(version=data["version"])
            if len(stress_version):
                return JsonResponse(code="999997", msg="存在相同版本号的测试记录")
            else:
                stressserializer = stressrecord_Deserializer(data=data)
                with transaction.atomic():
                    stressserializer.is_valid()
                    stressserializer.save()
                stressresult = sequence(data["loadserver"], end_time,testdata,
                                        data["version"],data["duration"],data["keyword"])
                return JsonResponse(data=stressresult, code="0", msg="成功")
        except Exception as e:
            print(e)
            return JsonResponse(msg="失败", code="999991", exception=e)


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
            obj = stress_record.objects.get(id=data["id"])
        except ObjectDoesNotExist:
            return JsonResponse(code="999995", msg="数据不存在！")
        # 查找是否相同名称
        pro_name = stress_record.objects.filter(content=data["content"]).exclude(id=data["id"])
        if len(pro_name):
            return JsonResponse(code="999997", msg="存在相同内容数据")
        else:
            serializer = stressrecord_Deserializer(data=data)
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

#获取 持续化数据
class getDuration(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def get(self, request):
        """
        获取持续话记录
        :param request:
        :return:
        """
        obi = duration.objects.filter().order_by("id")
        durationdata = duration_Serializer(obi,many=True)
        return JsonResponse(data={"data": durationdata.data
                                  }, code="0", msg="成功")

#保存dicom 发送记录
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
            if not data["dicom"] or not data["server"]:
                return JsonResponse(code="999996", msg="参数有误,必传参数 dicom, server！")

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
            data['dicom'] =','.join(data['dicom'])
            duration = duration_Deserializer(data=data)
            with transaction.atomic():
                duration.is_valid()
                duration.save()
            return JsonResponse(code="0", msg="成功")
        except ObjectDoesNotExist:
            return JsonResponse(code="999995", msg="数据不存在！")
#修改duration
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
            if not data["dicom"] or not data["server"]:
                return JsonResponse(code="999996", msg="参数有误,必传参数 dicom, server！")

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
            obj =duration.objects.get(id=data["id"])
            data['dicom'] =','.join(data['dicom'])
            serializer = duration_Deserializer(data=data)
            with transaction.atomic():
                if serializer.is_valid():
                    # 修改数据
                    serializer.update(instance=obj, validated_data=data)
            return JsonResponse(code="0", msg="成功")
        except ObjectDoesNotExist:
            return JsonResponse(code="999995", msg="数据不存在！")

#保存dicom 发送记录
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
            # 必传参数 key, server_ip , type
            if not data["dicom"] or not data["server"]:
                return JsonResponse(code="999996", msg="参数有误,必传参数 dicom, server！")

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
            duration = duration_Deserializer(data=data)
            with transaction.atomic():
                duration.is_valid()
                duration.save()
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
        # 查找项目是否存在
        try:
            obj = duration.objects.get(id=data["id"])
            obj.status = False
            obj.save()

            return JsonResponse(code="0", msg="成功")
        except ObjectDoesNotExist:
            return JsonResponse(code="999995", msg="项目不存在！")


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
            obj = duration.objects.get(id=data["id"])

            if obj.sendstatus is True:
                return JsonResponse(code="999994", msg="运行中！待停止后再启动！~")
            else:
                obj.status = True
                obj.sendstatus = True
                obj.save()
                for i in obj.dicom.split(","):
                    threading.Thread(target=send_duration,
                                      args=(obj,i)).start()
                    time.sleep(1)
                return JsonResponse(code="0", msg="成功")
        except ObjectDoesNotExist:
            return JsonResponse(code="999995", msg="运行失败！")



#删除dicom 数据
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
            delete_patients_duration(data['deldata'], data['server_ip'],data['testtype'], data['fuzzy'])
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
        data=verify()
        return JsonResponse(data={"data": data
                                  }, code="0", msg="成功")

