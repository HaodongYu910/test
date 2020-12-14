from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Sum,Min

from rest_framework.authentication import TokenAuthentication
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
import shutil,threading
from ..models import interface
from TestPlatform.common.api_response import JsonResponse
from TestPlatform.serializers import dicomdata_Deserializer,stress_Deserializer
from ..tools.stress.stress import *
from ..tools.stress.stresstest import lungSlice
from ..tools.orthanc.deletepatients import *
from ..tools.stress.stresstest import updateStressData
from ..tools.stress.PerformanceResult import *
import csv, os
import pandas as pd

logger = logging.getLogger(__name__)  # 这里使用 __name__ 动态搜索定义的 logger 配置


class stressversion(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def get(self, request):
        """
        获取压测记录
        :param request:
        :return:
        """
        server = request.GET.get("server", '192.168.1.208')
        obi = stress.objects.filter(loadserver__contains=server).order_by("-id")
        serialize = stress_Deserializer(obi, many=True)
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
        server = request.GET.get("server")
        slicenumber = request.GET.get("slicenumber")
        if diseases is not None and server is None and slicenumber is None:
            obi = dicom.objects.filter(diseases__contains=diseases).order_by("-id")
        elif server is not None and diseases is None and slicenumber is None:
            obi = dicom.objects.filter(server__contains=server).order_by("-id")
        elif server is not None and diseases is not None and slicenumber is None:
            obi = dicom.objects.filter(server__contains=server,diseases__contains=diseases).order_by("-id")
        elif slicenumber is not None and server is None:
            obi = dicom.objects.filter(slicenumber__contains=slicenumber).order_by("-id")
        elif slicenumber is not None and server is not None:
            obi = dicom.objects.filter(server__contains=server,slicenumber__contains=slicenumber).order_by("-id")
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

class addStressData(APIView):
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
            stresscache(data['id'])
            # thread_stress = threading.Thread(target=stresscache,args=(data['id']))
            # # 启动线程
            # thread_stress.start()
            return JsonResponse(code="0", msg="成功")
        except ObjectDoesNotExist:
            return JsonResponse(code="999995", msg="数据不存在！")

class addData(APIView):
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
            server=data['server']
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
                data['patientid']=patientid[0]['PatientID']
            try:
                data['vote'],SeriesInstanceUID = updateStressData(data['studyinstanceuid'], server)
            except ObjectDoesNotExist:
                return JsonResponse(code="999994", msg="数据未预测，请先预测！")

            if data['diseases'] =='Lung':
                data['imagecount'],data['slicenumber'], = lungSlice(server, SeriesInstanceUID)
                data['predictor'] ='lungct_predictor'
            elif data['diseases'] in ['Brain','SVD','SWI','Tumor','post_surgery']:
                data['predictor'] = 'brainmri_predictor'
            elif data['diseases'] =='Breast':
                data['predictor'] = 'breastmri_predictor'
            elif data['diseases'] == 'coronary':
                data['predictor'] = 'corocta_predictor'
            elif data['diseases'] =='CTA':
                data['predictor'] = 'braincta_predictor'
            elif data['diseases'] =='CTP':
                data['predictor'] = 'brainctp_predictor'
            elif data['diseases'] == 'Hematoma':
                data['predictor'] = 'brainct_predictor'
            elif data['diseases'] == 'Heart':
                data['predictor'] = 'heartmri_predictor'
            elif data['diseases'] == 'Neck':
                data['predictor'] = 'archcta_predictor'
            elif data['diseases'] == 'MRA':
                data['predictor'] = 'brainctp_predictor'

            dicomdata = dicomdata_Deserializer(data=data)

            with transaction.atomic():
                dicomdata.is_valid()
                dicomdata.save()
            return JsonResponse(code="0", msg="成功")
        except ObjectDoesNotExist:
            return JsonResponse(code="999995", msg="数据不存在！")


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
            prediction = stress_result.objects.filter(version=data['version'], type__in=['prediction','lung_prediction'])
            job = stress_result.objects.filter(version=data['version'], type__in=['job','lung_job'])

            predictionb = stress_result.objects.filter(version=data['checkversion'], type__in=['prediction','lung_prediction'])
            jobb = stress_result.objects.filter(version=data['checkversion'], type__in=['job','lung_job'])

            predictionresult = dataCheck(prediction, predictionb)
            jobresult = dataCheck(job, jobb)
            diffresult = dataCheck(job,prediction)
            return JsonResponse(data={"predictionresult": predictionresult,
                                              "jobresult": jobresult,
                                              "diffresult":diffresult
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
            if not data["id"]:
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
            obj = stress.objects.get(id=data['id'])
            checkdate = [obj.start_date, obj.end_date]
            if obj.projectname=='晨曦':

                savecheck('prediction', checkdate, obj.loadserver, obj.version)
                lung(checkdate, obj.loadserver, obj.version)
                savecheck('job', checkdate, obj.loadserver, obj.version)
            elif obj.projectname=='肺炎':
                lung(checkdate, obj.loadserver, obj.version)

            return JsonResponse( code="0", msg="成功")
        except Exception as e:
            return JsonResponse(msg="失败", code="999991", exception=e)


# 预测压力测试运行
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
            # 必传参数 loadserver, dicom, loop_time
            if not data["id"]:
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

            obj = stress.objects.get(id =data['id'])
            if obj.start_date is None:
                obj.start_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                obj.save()
            else:
                obj.update_time =datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                obj.save()
            if data['type'] is True:
                Manual(obj.loadserver,obj.testdata,obj.loop_count)
            else:
                AutoPrediction(obj.loadserver,obj.testdata,obj.loop_count)
            return JsonResponse(code="0", msg="运行成功")
        except Exception as e:
            logger.error(e)
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


# 性能测试数据
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
            obi = stress.objects.filter(version=version,status=True).order_by("-id")
        else:
            obi = stress.objects.all().order_by("-id")
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
            model = ''
            # id 转换成病种文案
            for j in i["testdata"].split(","):
                obj = dictionary.objects.get(id=j)
                model = model + obj.value + ","
            i["testdata"] = model
            i["type"] =False
        return JsonResponse(data={"data":serialize.data,
                                  "page": page,
                                  "total": total,
                                  "count": count
                                  }, code="0", msg="成功")


class stressDetail(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def get(self,request,format=None):
        """
                获取压测详情
                :param request:
                :return:
                """
        try:
            id = request.GET.get("id")
            obj = stress.objects.filter(id=id)
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
            if not data["testdata"] or not data["loadserver"]or not data["version"]:
                return JsonResponse(code="999996", msg="参数有误,必传参数 stress, loadserver！")

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
            data["testdata"] =str(data["testdata"])[1:-1]
            Stressadd = stress_Deserializer(data=data)

            with transaction.atomic():
                Stressadd.is_valid()
                Stressadd.save()
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
            data["testdata"] =str(data["testdata"])[1:-1]
            obj = stress.objects.get(id=data["id"])
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
            obj = stress.objects.get(id=data["id"])
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
            obj = stress.objects.get(id=data["id"])
            obj.status = True
            obj.save()

            return JsonResponse(code="0", msg="成功")
        except ObjectDoesNotExist:
            return JsonResponse(code="999995", msg="不存在！")



# 删除dicom 发送记录
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
                    obj = stress.objects.get(id=i)
                    try:
                        obj.delete()
                    except ObjectDoesNotExist:
                        return JsonResponse(code="999994", msg="删除失败！")
                    return JsonResponse(code="0", msg="成功")
                except ObjectDoesNotExist:
                    return JsonResponse(code="999995", msg="数据不存在！")

        except ObjectDoesNotExist:
            return JsonResponse(code="999995", msg="执行失败！")


class StressUpload(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def post(self, request):
        """
        启用项目
        :param request:
        :return:
        """
        try:
            url = '/files/stress'
            File = request.FILES.get("file", None)
            with open("{0}/{1}".format(url,File.name) , 'wb+') as f:
                # 分块写入文件
                for chunk in File.chunks():
                    f.write(chunk)
            data={
                "interfacename":File.name,
                "json":url,
                "type":"stress",
                "status":True
            }
            filedata=interface.objects.create(**data)
            return JsonResponse(code="0", msg="成功",data=filedata.id)
        except ObjectDoesNotExist:
            return JsonResponse(code="999995", msg="没有需要上传的文件！")
