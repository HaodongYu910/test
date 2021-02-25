from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from ..models import stress_result, base_data ,pid

from rest_framework.authentication import TokenAuthentication
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
import threading
from ..common.api_response import JsonResponse
from ..common.dicomBase import baseTransform
from ..serializers import dicomdata_Deserializer, stress_Deserializer, stress_record_Serializer
from ..tools.stress.stress import *
from ..tools.orthanc.deletepatients import *
from ..tools.stress.PerformanceResult import *
from ..tools.stress.stressfigure import stressdataFigure
from ..tools.dicom.dicomdetail import anonymousSend

logger = logging.getLogger(__name__)  # 这里使用 __name__ 动态搜索定义的 logger 配置


# 获取性能测试版本
class stressversion(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def get(self, request):
        """
        获取压测记录
        :param request:
        :return:
        """

        obi = stress.objects.filter(status=1).order_by("-stressid")
        serialize = stress_Deserializer(obi, many=True)
        # for i in obi.version:
        #     dict = {'key': i, 'value': i}
        #     list.append(dict)
        return JsonResponse(data={"data": serialize.data
                                  }, code="0", msg="成功")

# 性能测试数据
class stressData(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def get(self, request):
        """
        获取性能数据
        :param request:
        :return:
        """
        try:
            page_size = int(request.GET.get("page_size", 20))
            page = int(request.GET.get("page", 1))
        except (TypeError, ValueError):
            return JsonResponse(code="999985", msg="page and page_size must be integer!")
        diseases = request.GET.get("diseases")
        slicenumber = request.GET.get("slicenumber")
        if diseases is not None and slicenumber is None:
            obi = dicom.objects.filter(predictor=diseases,stressstatus__in=(1,2)).order_by("-id")
        elif diseases is None and slicenumber is not None:
            obi = dicom.objects.filter(slicenumber=slicenumber,stressstatus__in=(1,2)).order_by("-id")
        else:
            obi = dicom.objects.filter(stressstatus__in=(1,2)).order_by("-id")
        paginator = Paginator(obi, page_size)  # paginator对象
        total = paginator.num_pages  # 总页数
        try:
            obm = paginator.page(page)
        except PageNotAnInteger:
            obm = paginator.page(1)
        except EmptyPage:
            obm = paginator.page(paginator.num_pages)
        serialize = dicomdata_Deserializer(obm, many=True)
        for i in serialize.data:
            dictobj = dictionary.objects.get(id=i["predictor"])
            i["diseases"] = dictobj.value

        return JsonResponse(data={"data": serialize.data,
                                  "page": page,
                                  "total": total
                                  }, code="0", msg="成功")

# 添加性能测试数据
class AddStressData(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def parameter_check(self, data):
        """
        校验参数
        :param data:
        :return:
        """
        try:
            # 必传参数 ids
            if not data["ids"]:
                return JsonResponse(code="999996", msg="参数有误,必传参数 ids！")

        except KeyError:
            return JsonResponse(code="999996", msg="参数ids有误！")

    def post(self, request):
        """
        添加压测数据
        :param request:
        :return:
        """
        data = JSONParser().parse(request)
        result = self.parameter_check(data)
        if result:
            return result
        try:
            for i in data["ids"]:
                obj = dicom.objects.get(id=i)
                obj.stressstatus = 1
                obj.save()
            return JsonResponse(code="0", msg="成功")
        except ObjectDoesNotExist:
            return JsonResponse(code="999995", msg="数据不存在！")

# 同步性能测试数据
class SynchroStressData(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def parameter_check(self, data):
        """
        校验参数
        :param data:
        :return:
        """
        try:
            # 必传参数 ids
            if not data["ids"]:
                return JsonResponse(code="999996", msg="参数有误,必传参数 ids！")

        except KeyError:
            return JsonResponse(code="999996", msg="参数ids有误！")

    def post(self, request):
        """
        同步压测数据
        :param request:
        :return:
        """
        data = JSONParser().parse(request)
        result = self.parameter_check(data)
        if result:
            return result
        try:
            kc = login_keycloak(1)
            for i in data["ids"]:
                obj = stress_record.objects.get(recordid=i)
                try:
                    checkuid(1, '192.168.1.208', obj.stressid)
                except ObjectDoesNotExist:
                    logger.error("数据问题{0}".format(obj.studyuid))
                obj.graphql, obj.imagecount, obj.slicenumber = voteData(obj.studyuid, '192.168.1.208', obj.diseases, kc)
                obj.save()
            return JsonResponse(code="0", msg="成功")
        except ObjectDoesNotExist:
            return JsonResponse(code="999995", msg="数据不存在！")

# 删除性能测试数据
class DelStressData(APIView):
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
            if not isinstance(data["ids"], list):
                return JsonResponse(code="999996", msg="参数有误！")
            for i in data["ids"]:
                if not isinstance(i, int):
                    return JsonResponse(code="999996", msg="参数有误！")
        except KeyError:
            return JsonResponse(code="999996", msg="参数有误！")

    def post(self, request):
        """
        删除压测数据
        :param request:
        :return:
        """
        data = JSONParser().parse(request)
        result = self.parameter_check(data)
        if result:
            return result
        try:
            for j in data["ids"]:
                try:
                    obj = dicom.objects.get(id=j)
                    obj.stressstatus = 0
                    obj.save()
                except Exception as e:
                    return JsonResponse(code="999998", msg="删除失败")
            return JsonResponse(code="0", msg="成功")
        except ObjectDoesNotExist:
            return JsonResponse(code="999995", msg="数据不存在！")

#  Disable基准数据
class DisableBenchmarkStatus(APIView):
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
            obj = dicom.objects.get(id=data["id"])
            obj.stressstatus = 1
            obj.save()
            return JsonResponse(code="0", msg="成功")
        except ObjectDoesNotExist:
            return JsonResponse(code="999995", msg="不存在！")


# Enable 基准数据
class EnableBenchmarkStatus(APIView):
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
            obj = dicom.objects.get(id=data["id"])
            obj.stressstatus = 2
            obj.save()

            return JsonResponse(code="0", msg="成功")
        except ObjectDoesNotExist:
            return JsonResponse(code="999995", msg="不存在！")


# 压测结果返回接口
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
            type = data["type"]
            if type == 'jz':
                prediction = stress_result.objects.filter(version=data['version'],
                                                          type__in=['predictionJZ', 'lung_prediction'])
                job = stress_result.objects.filter(version=data['version'], type__in=['jobJZ', 'lung_jobJZ'])

                predictionb = stress_result.objects.filter(version=data['checkversion'],
                                                           type__in=['predictionJZ', 'lung_JZ'])
                jobb = stress_result.objects.filter(version=data['checkversion'], type__in=['jobJZ', 'lung_jobJZ'])

                predictionresult = dataCheck(prediction, predictionb)
                jobresult = dataCheck(job, jobb)
                diffresult = dataCheck(job, prediction)
            elif type == 'dy':
                prediction = stress_result.objects.filter(version=data['version'],
                                                          type__in=['predictiondy', 'lung_dy'])
                job = stress_result.objects.filter(version=data['version'], type__in=['jobdy', 'lung_jobdy'])

                predictionb = stress_result.objects.filter(version=data['checkversion'],
                                                           type__in=['predictiondy', 'lung_dy'])
                jobb = stress_result.objects.filter(version=data['checkversion'], type__in=['jobdy', 'lung_jobdy'])

                predictionresult = dataCheck(prediction, predictionb)
                jobresult = dataCheck(job, jobb)
                diffresult = dataCheck(job, prediction)
            else:
                prediction = stress_result.objects.filter(version=data['version'],
                                                          type__in=['prediction', 'lung_prediction'])
                job = stress_result.objects.filter(version=data['version'], type__in=['job', 'lung_job'])

                predictionb = stress_result.objects.filter(version=data['checkversion'],
                                                           type__in=['prediction', 'lung_prediction'])
                jobb = stress_result.objects.filter(version=data['checkversion'], type__in=['job', 'lung_job'])

                predictionresult = dataCheck(prediction, predictionb)
                jobresult = dataCheck(job, jobb)
                diffresult = dataCheck(job, prediction)
            return JsonResponse(data={"predictionresult": predictionresult,
                                      "jobresult": jobresult,
                                      "diffresult": diffresult
                                      }, code="0", msg="成功")

        except Exception as e:
            return JsonResponse(msg="失败", code="999991", exception=e)


# 保存压力测试预测性能结果
class stressResultsave(APIView):
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
            if not data["stressid"]:
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
            Sf = StressThread(stressid=data['stressid'])
            Sf.SaveResult()
            Sf.SaveRecord()

            return JsonResponse(code="0", msg="成功")
        except Exception as e:
            return JsonResponse(msg="失败", code="999991", exception=e)


# 运行压力测试运行
class stressRun(APIView):
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
                anonymous = threading.Thread(target=anonymousSend, args=(data['stressid'], 'stress'))
                anonymous.start()
            return JsonResponse(code="0", msg="运行成功")
        except Exception as e:
            logger.error(e)
            return JsonResponse(msg="失败", code="999991", exception=e)

# 压力测试停止
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
        执行压测脚本
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

# 获取性能测试数据
class getStressdata(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def get(self, request):
        """
        获取持续话记录
        :param request:
        :return:
        """
        obi = stress.objects.all().order_by("server")
        stressdata = stress_Deserializer(obi, many=True)
        du = stressdata.data
        for i in du:
            obj = stress_record.objects.filter(stress_id=i["id"],
                                               create_time__gte=i["update_time"])
            i['send'] = str(obj.count())

        return JsonResponse(data={"data": stressdata.data
                                  }, code="0", msg="成功")


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


# 性能图表
class reportfigure(APIView):
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
            if not data["type"]:
                return JsonResponse(code="999996", msg="缺失必要参数,参数 type！")

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
            type = data["type"]
            if type == 'jz':
                predictionData, jobData, lungData, lungjobData = map(stressdataFigure,
                                                                     ["predictionJZ", "jobJZ", "lung_JZ",
                                                                      "lung_jobJZ"])
            elif type == 'dy':
                predictionData, jobData, lungData, lungjobData = map(stressdataFigure,
                                                                     ["predictiondy", "jobdy", "lung_dy",
                                                                      "lung_jobdy"])
            else:
                predictionData, jobData, lungData, lungjobData = map(stressdataFigure,
                                                                     ["prediction", "job", "lung_prediction",
                                                                      "lung_job"])

            return JsonResponse(data={"modlename": predictionData[1],
                                      "lungname": lungData[1],
                                      "predictionFigure": predictionData[0],
                                      "jobFigure": jobData[0],
                                      "lungFigure": lungData[0],
                                      "lungjobFigure": lungjobData[0]
                                      }, code="0", msg="成功")
        except Exception as e:
            return JsonResponse(msg="失败", code="999991", exception=e)
