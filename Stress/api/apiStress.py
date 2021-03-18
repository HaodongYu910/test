from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from TestPlatform.models import pid

from rest_framework.authentication import TokenAuthentication
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from TestPlatform.common.api_response import JsonResponse
from ..serializers import  stress_Deserializer
from ..common.stress import *
from ..common.PerformanceResult import *
from Dicom.common.dicomBase import baseTransform
from Dicom.common.deletepatients import *
from Dicom.common.Dicom import DicomThread

logger = logging.getLogger(__name__)  # 这里使用 __name__ 动态搜索定义的 logger 配置


class stressRun(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def parameter_check(self, data):
        """
        验证参数
        :运行压力测试运行
        :return:
        """
        try:
            # 必传参数 stressid
            if not data["stressid"]:
                return JsonResponse(code="999996", msg="缺失必要参数,参数 loadserver, dicom, loop_time！")

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
            obj = stress.objects.get(stressid=data['stressid'])
            St = StressThread(stressid=data['stressid'])
            # 基准测试
            if data['type'] is True:
                resultobj = stress_result.objects.filter(stressid=data['stressid'],type__in=['jobJZ','predictionJZ','lung_jobJZ','lung_job'])
                resultobj.delete()
                St.Manual()
            # 混合测试
            elif data['type'] is False:
                if obj.jmeterstatus is True:
                    St.jmeterStress()
                # St.AutoPrediction()
                St.AutoPrediction(type='send')
            # 单一测试
            else:
                if obj.jmeterstatus is True:
                    St.jmeterStress()
                anonymous = DicomThread(stressid=data['stressid'], type='stress')
                anonymous.start()
            return JsonResponse(code="0", msg="运行成功")
        except Exception as e:
            logger.error(e)
            return JsonResponse(msg="失败", code="999991", exception=e)


class stressStop(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def parameter_check(self, data):
        """
        验证参数
        :param data:
        :return:
        """
        try:
            # 必传参数 stressid
            if not data["stressid"]:
                return JsonResponse(code="999996", msg="缺失必要参数,参数 loadserver, dicom, loop_time！")

        except KeyError:
            return JsonResponse(code="999996", msg="参数有误！")

    def post(self, request):
        """
        停止压力测试
        :param request:
        :return:
        """
        data = JSONParser().parse(request)
        result = self.parameter_check(data)
        if result:
            return result
        try:
            stoptest = StressThread(stressid=data["stressid"])
            # 设为保护线程，主进程结束会关闭线程
            stoptest.setFlag = False
            durationid = '0'+str(data["stressid"])
            obj = pid.objects.filter(durationid=durationid)
            # kill 线程
            for i in obj:
                cmd = 'kill -9 {0}'.format(int(i.pid))
                logger.info(cmd)
                os.system(cmd)
                i.delete()
            drobj = duration_record.objects.filter(duration_id=durationid, imagecount=None)
            # # 删除错误数据
            # for j in drobj:
            #     delete_patients_duration(j.studyinstanceuid, okj.hostid, "studyinstanceuid", False)
            # drobj.delete()
            # # 删除 文件夹
            # folder = "/home/biomind/Biomind_Test_Platform/logs/{0}{1}{2}".format(str(okj.patientname),
            #                                                                      str(okj.patientid),
            #                                                                      str(okj.id))
            # if os.path.exists(folder):
            #     shutil.rmtree(folder)

            return JsonResponse(code="0", msg="已停止")
        except Exception as e:
            logger.error(e)
            return JsonResponse(msg="失败", code="999991", exception=e)

# 获取压测列表
class stressList(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def get(self, request):
        """
        获取性能列表数据
        :param request:
        :return:
        """
        try:
            page_size = int(request.GET.get("page_size", 20))
            page = int(request.GET.get("page", 1))
        except (TypeError, ValueError):
            return JsonResponse(code="999985", msg="page and page_size must be integer!")
        version = request.GET.get("version")

        # 判断查询数据类型
        if version:
            obi = stress.objects.filter(version=version, status=True).order_by("-stressid")
        else:
            obi = stress.objects.all().order_by("-stressid")
        paginator = Paginator(obi, page_size)  # paginator对象
        total = paginator.num_pages  # 总页数
        count = paginator.count  # 总页数
        try:
            obm = paginator.page(page)
        except PageNotAnInteger:
            obm = paginator.page(1)
        except EmptyPage:
            obm = paginator.page(paginator.num_pages)
        serialize = stress_Deserializer(obm, many=True)
        for i in serialize.data:
            i["testdata"] = baseTransform(i["testdata"],'dictionary')
            i["type"] = False
        return JsonResponse(data={"data": serialize.data,
                                  "page": page,
                                  "total": total,
                                  "count": count
                                  }, code="0", msg="成功")

# 压测详情
class stressDetail(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def get(self, request):
        """
                获取压测详情
                :param request:
                :return:
                """
        try:
            stressid = request.GET.get("stressid")
            obj = stress.objects.filter(stressid=stressid)
            stressserializer = stress_Deserializer(obj, many=True)

            return JsonResponse(data={"data": stressserializer.data
                                      }, code="0", msg="成功")
        except Exception as e:
            logger.error(e)
            return JsonResponse(msg="失败", code="999991", exception=e)


# 保存性能测试记录
class addStress(APIView):
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
            if not data["testdata"] or not data["hostid"] or not data["version"]:
                return JsonResponse(code="999996", msg="参数有误,必传参数 version, hostid！")

        except KeyError:
            return JsonResponse(code="999996", msg="参数有误,必传参数 version, hostid testdata！！")

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
            hostobj = GlobalHost.objects.get(id=data['hostid'])
            data["loadserver"] = hostobj.host
            data["testdata"] = str(data["testdata"])[1:-1]
            Stressadd = stress_Deserializer(data=data)
            with transaction.atomic():
                Stressadd.is_valid()
                strdata = Stressadd.save()
                dict = data['filedict']
                if dict != {}:
                    for k, v in dict.items():
                        try:
                            obj = uploadfile.objects.get(id=v)
                            obj.fileid = str(strdata.stressid)
                            obj.save()
                        except Exception as e:
                            logger.error("更新upload数据失败{0},错误：{1}".format(v, e))
                            continue
                    obj = stress.objects.get(stressid=strdata.stressid)
                    obj.jmeterstatus = True
                    obj.save()
            return JsonResponse(code="0", msg="成功")
        except Exception as e:
            return JsonResponse(code="999995", msg="{0}".format(e))


# 修改压测信息
class updateStress(APIView):
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
            if not data["stressid"]:
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
            try:
                # hostobj = GlobalHost.objects.get(id=data['hostid'])
                # data["loadserver"] = hostobj.host
                # data["testdata"] = str(data["testdata"])[1:-1]
                dict = data['filedict']
                for k, v in dict.items():
                    obj = uploadfile.objects.get(id=v)
                    obj.fileid = str(data["id"])
                    obj.save()
            except Exception as e:
                return JsonResponse(code="999991", msg="更新upload数据失败{0}".format(e))

            obj = stress.objects.get(stressid=data["stressid"])
            serializer = stress_Deserializer(data=data)
            with transaction.atomic():
                if serializer.is_valid():
                    # 修改数据
                    serializer.update(instance=obj, validated_data=data)
            return JsonResponse(code="0", msg="成功")
        except ObjectDoesNotExist:
            return JsonResponse(code="999995", msg="数据不存在！")


class DisableStress(APIView):
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
        禁用项目
        :param request:
        :return:
        """
        data = JSONParser().parse(request)
        result = self.parameter_check(data)
        if result:
            return result
        # 查找是否存在
        try:
            obj = stress.objects.get(stressid=data["stressid"])
            obj.status = False
            obj.save()
            return JsonResponse(code="0", msg="成功")
        except ObjectDoesNotExist:
            return JsonResponse(code="999995", msg="不存在！")


class EnableStress(APIView):
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
            obj = stress.objects.get(stressid=data["stressid"])
            obj.status = True
            obj.save()

            return JsonResponse(code="0", msg="成功")
        except ObjectDoesNotExist:
            return JsonResponse(code="999995", msg="不存在！")

# 删除 性能测试
class delStress(APIView):
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
                    obj = stress.objects.get(stressid=i)
                    try:
                        obj.delete()
                    except ObjectDoesNotExist:
                        return JsonResponse(code="999994", msg="删除失败！")
                    return JsonResponse(code="0", msg="成功")
                except ObjectDoesNotExist:
                    return JsonResponse(code="999995", msg="数据不存在！")

        except ObjectDoesNotExist:
            return JsonResponse(code="999995", msg="执行失败！")


