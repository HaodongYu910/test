from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Sum,Min

from rest_framework.authentication import TokenAuthentication
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
import shutil

from TestPlatform.common.api_response import JsonResponse
from TestPlatform.models import stress_record,dicom, base_data, pid, GlobalHost
from TestPlatform.serializers import stressrecord_Deserializer, \
    dicomdata_Deserializer, duration_Deserializer
from ..tools.stress.stress import sequence
from ..tools.stress.stresstest import stress,lungSlice
from ..tools.orthanc.deletepatients import *
from ..tools.dicom.duration_verify import *
from ..tools.stress.stresstest import updateStressData
from ..tools.stress.PerformanceResult import *

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

class addstressdata(APIView):
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


# 修改duration
class updatestressdata(APIView):
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

# 删除dicom 数据
class delstressdata(APIView):
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
            prediction = stress_result.objects.filter(version=data['version'], type='prediction')
            job = stress_result.objects.filter(version=data['version'], type='job')
            lung = stress_result.objects.filter(version=data['version'], type='lung')

            predictionobj = stress_result.objects.filter(version=data['checkversion'], type='prediction')
            jobobj = stress_result.objects.filter(version=data['checkversion'], type='job')
            lungobj = stress_result.objects.filter(version=data['checkversion'], type='lung')

            predictionresult = dataCheck(prediction, predictionobj)
            jobresult = dataCheck(job, jobobj)
            lungresult = dataCheck(lung, lungobj)

            return JsonResponse(data={"predictionresult": predictionresult,
                                      "jobresult": jobresult,
                                      "lungresult": lungresult
                                      }, code="0", msg="成功")
        except Exception as e:
            return JsonResponse(msg="失败", code="999991", exception=e)


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
            if not data["version"]:
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
            obj = stress_record.objects.get(version=data['version'])
            checkdate = [obj.start_date, obj.end_date]
            # savecheck('job', checkdate, obj.loadserver, obj.version)
            # savecheck('prediction', checkdate, obj.loadserver, obj.version)
            lung(checkdate, obj.loadserver, obj.version)

            return JsonResponse(data={"data": ''}, code="0", msg="成功")
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
            # 必传参数 loadserver, dicom, loop_time
            if not data["loadserver"] or not data["testdata"] or not data["loop_time"]:
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
            testdata = data["testdata"]
            # 查找是否相同版本号的测试记录
            stress_version = stress_record.objects.filter(version=data["version"])
            if len(stress_version):
                return JsonResponse(code="999997", msg="存在相同版本号的测试记录")
            else:
                if data['switch'] is True:
                    for j in testdata:
                        dicom = base_data.objects.get(remarks=j)
                        folder = dicom.content
                        cmd = ('nohup /home/biomind/.local/share/virtualenvs/biomind-dvb8lGiB/bin/python3'
                               ' /home/biomind/Biomind_Test_Platform/TestPlatform/tools/duration/Stress.py '
                               '--ip {0} --aet {1} '
                               '--port {2} '
                               '--keyword {3} '
                               '--dicomfolder {4} '
                               '--diseases {5} '
                               '--end {6} > /home/biomind/Biomind_Test_Platform/logs/stress{7}.log 2&>1 &').format(data['loadserver'],'orthanc208', '4242','stress', folder, j,
                                                     data['loop_time'],j)
                        logger.info(cmd)
                        os.system(cmd)
                        time.sleep(1)
                try:
                    stress(data["loadserver"], testdata,data["version"],data["thread"],data["loop"],data["synchronizing"],0,'23400')
                except Exception as e:
                    logger.error(e)
                    return JsonResponse(msg="jmeter执行失败", code="999991", exception=e)
                data['testdata'] = str(testdata)
                data['start_date'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                data['end_date'] = (datetime.datetime.now() + datetime.timedelta(hours=int(data["loop_time"]))).strftime(
                    "%Y-%m-%d %H:%M:%S")
                stressserializer = stressrecord_Deserializer(data=data)
                with transaction.atomic():
                    stressserializer.is_valid()
                    stressserializer.save()
                return JsonResponse(code="0", msg="成功")
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
        obi = duration.objects.all().order_by("server")
        durationdata = duration_Serializer(obi, many=True)
        du = durationdata.data
        for i in du:
            obj = duration_record.objects.filter(duration_id=i["id"],
                                                 create_time__gte=i["update_time"])
            i['send'] = str(obj.count())

        return JsonResponse(data={"data": durationdata.data
                                  }, code="0", msg="成功")


# 获取 持续化发送详细数据
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
            obi = stress_record.objects.filter(version=version,status=True).order_by("-id")
        else:
            obi = stress_record.objects.filter(status=True).order_by("-id")
        paginator = Paginator(obi, page_size)  # paginator对象
        total = paginator.num_pages  # 总页数
        count = paginator.count  # 总页数
        try:
            obm = paginator.page(page)
        except PageNotAnInteger:
            obm = paginator.page(1)
        except EmptyPage:
            obm = paginator.page(paginator.num_pages)
        serialize = stressrecord_Deserializer(obm, many=True)
        return JsonResponse(data={"data": serialize.data,
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
            obj = stress_record.objects.filter(id=id)
            stressserializer = stressrecord_Deserializer(obj, many=True)

            return JsonResponse(data={"data": stressserializer.data
                                          }, code="0", msg="成功")
        except Exception as e:
            logger.error(e)
            return JsonResponse(msg="失败", code="999991", exception=e)

# 保存dicom 发送记录
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


