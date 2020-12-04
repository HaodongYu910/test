from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Sum,Min

from rest_framework.authentication import TokenAuthentication
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
import threading

from TestPlatform.common.api_response import JsonResponse
from TestPlatform.models import stress, dicom, base_data, pid, GlobalHost,dicom_record
from TestPlatform.serializers import stressrecord_Deserializer, \
    dicomdata_Deserializer, duration_Deserializer
from ..tools.smoke.gold import *
from ..tools.stress.stresstest import lungSlice
from ..tools.orthanc.deletepatients import *
from ..tools.dicom.duration_verify import *
from ..tools.stress.stresstest import updateStressData
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
                    dicomdata = dicom.objects.filter(vote=None,diseases=data['diseases'])
                else:
                   dicomdata=dicom.objects.filter(vote=None)
                for i in dicomdata:
                    try:
                        i.vote,i.imagecount,i.slicenumber = voteData(i.studyinstanceuid,server,i.diseases)
                        i.save()
                    except Exception as  e :
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
            obi = dicom.objects.filter(diseases__contains=diseases,type=type).order_by("-id")
        elif server is not None and diseases is None and slicenumber is None:
            obi = dicom.objects.filter(server__contains=server,type=type).order_by("-id")
        elif server is not None and diseases is not None and slicenumber is None:
            obi = dicom.objects.filter(server__contains=server,type=type,diseases__contains=diseases).order_by("-id")
        elif slicenumber is not None and server is None:
            obi = dicom.objects.filter(slicenumber__contains=slicenumber,type=type).order_by("-id")
        elif slicenumber is not None and server is not None:
            obi = dicom.objects.filter(server__contains=server,type=type,slicenumber__contains=slicenumber).order_by("-id")
        elif type is not None:
            obi = dicom.objects.all().order_by("-id")
        else:
            obi = dicom.objects.filter(type=type).order_by("-id")
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

class somkeRecord(APIView):
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
        version = request.GET.get("version")
        server = request.GET.get("server")
        status = request.GET.get("status")
        if version is not None and server is None and status is None:
            obi = dicom_record.objects.filter(version__contains=version).order_by("-id")
        elif server is not None and version is None and status is None:
            obi = dicom_record.objects.filter(server__contains=server).order_by("-id")
        elif server is not None and version is not None and status is None:
            obi = dicom_record.objects.filter(server__contains=server,diseases__contains=version).order_by("-id")
        elif status is not None and server is None:
            obi = dicom_record.objects.filter(status__contains=status).order_by("-id")
        elif status is not None and server is not None:
            obi = dicom_record.objects.filter(server__contains=server,status__contains=status).order_by("-id")
        else:
            obi = dicom_record.objects.all().order_by("-id")
        paginator = Paginator(obi, page_size)  # paginator对象
        total = paginator.num_pages  # 总页数
        try:
            obm = paginator.page(page)
        except PageNotAnInteger:
            obm = paginator.page(1)
        except EmptyPage:
            obm = paginator.page(paginator.num_pages)
        serialize = dicomrecord_Serializer(obm, many=True)
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
class updatedicomdata(APIView):
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
            if not data["server_ip"]:
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
            if data['ids']:
                obj = dicom.objects.filter(fileid__in=data['ids'])
            else:
                obj = dicom.objects.filter(id__in=data['id'])
            for i in obj:
                Send(data["server_ip"], i.route)

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
            delreport(data['server'],data["ids"])
            return JsonResponse(code="0", msg="执行成功")
        except ObjectDoesNotExist:
            return JsonResponse(code="999995", msg="数据不存在！")


class SomkeTest(APIView):
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
            if not data["server_ip"] or not data["version"] :
                return JsonResponse(code="999996", msg="缺失必要参数,参数 server, ids！")

        except KeyError:
            return JsonResponse(code="999996", msg="参数有误！")

    def post(self, request):
        """
        执行脚本
        :param request:
        :return:
        """
        data = JSONParser().parse(request)
        result = self.parameter_check(data)
        if result:
            return result

        try:
            # 查找是否相同版本号的测试记录
            dicom_version = dicom_record.objects.filter(version=data["version"])
            try:
                ids =[]
                ides = []
                if data['diseases']:
                    obj = base_data.objects.filter(remarks=data['diseases'],type='Gold')
                else:
                    obj = base_data.objects.filter(type='Gold',status=True)
                for i in obj:ids.append(i.id)
                dicomobj = dicom.objects.filter(fileid__in=ids)
                for j in dicomobj:ides.append(j.id)
                thread_fake_folder = threading.Thread(target=goldSmoke,
                                                      args=(data["version"], data["server_ip"],ides))
                # 启动线程
                thread_fake_folder.start()
            except Exception as e:
                logger.error(e)
                return JsonResponse(msg="执行失败", code="999991", exception=e)
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
            obj = stress.objects.get(id=data["id"])
        except ObjectDoesNotExist:
            return JsonResponse(code="999995", msg="数据不存在！")
        # 查找是否相同名称
        pro_name = stress.objects.filter(content=data["content"]).exclude(id=data["id"])
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





