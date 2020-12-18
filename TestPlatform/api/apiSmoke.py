
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


from rest_framework.authentication import TokenAuthentication
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
import threading

from TestPlatform.common.api_response import JsonResponse
from TestPlatform.models import dicom_record, base_data
from TestPlatform.serializers import dicomrecord_Serializer,dicomrecord_Deserializer
from ..tools.smoke.gold import *
from ..tools.orthanc.deletepatients import *
from ..tools.dicom.duration_verify import *
from ..tools.stress.PerformanceResult import *
from ..tools.dicom.dicomdetail import delFolder

logger = logging.getLogger(__name__)  # 这里使用 __name__ 动态搜索定义的 logger 配置

class smokeRecord(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def get(self, request):
        """
        获取冒烟数据显示数据列表
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
        if  request.GET.get("status")=='true':
            status = 1
        elif request.GET.get("status")=='False':
            status = 0
        else:
            status = ''

        diseases = request.GET.get("diseases")
        if version != '' and server != '' and status != '':
            obi = dicom_record.objects.filter(version__contains=version,status= status).order_by("-id")
        elif version == '' and server != '' and status != '':
            obi = dicom_record.objects.filter(server__contains=server,status = status).order_by("-id")
        elif version == '' and server == '' and status != '':
            obi = dicom_record.objects.filter(status=status).order_by("-id")
        elif version == '' and server != '' and status == '':
            obi = dicom_record.objects.filter(server=server).order_by("-id")
        elif version == '' and server == '' and status != '':
            obi = dicom_record.objects.filter(server__contains=server,status=status).order_by("-id")
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
        for i in serialize.data:
            # 求预测时间
            if i['completiontime'] is not None and i['starttime'] is not None:
                completiontime = time.strptime(str(i['completiontime']), "%Y-%m-%d %H:%M:%S")
                starttime = time.strptime(str(i['starttime']), "%Y-%m-%d %H:%M:%S")
                i['time'] = int(time.mktime(completiontime)) - int(time.mktime(starttime))
        return JsonResponse(data={"data": serialize.data,
                                  "page": page,
                                  "total": total
                                  }, code="0", msg="成功")


class smokeTest(APIView):
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
                # goldSmoke(data["version"], data["server_ip"],ides)
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


class smokefigure(APIView):
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
            # modlename =['aibrainct', 'aibrainmri', 'aicardiomodel', 'archcta',
            #                 'brainctp','headcta', 'postsurgery','brainmra']
            # lungname = ['0.9','1.0','1.25','1.5','5.0','10.0']
            predictionData,modlename =stressdataFigure("prediction")
            jobData,modlename = stressdataFigure("job")

            lungData,lungname =stressdataFigure("lung_prediction")
            lungjobData,lungname = stressdataFigure("lung_job")

            return JsonResponse(data={"modlename":modlename,
                                      "lungname":lungname,
                                      "predictionFigure": predictionData,
                                     "jobFigure": jobData,
                                      "lungFigure":lungData,
                                      "lungjobFigure":lungjobData
                                      }, code="0", msg="成功")
        except Exception as e:
            return JsonResponse(msg="失败", code="999991", exception=e)
