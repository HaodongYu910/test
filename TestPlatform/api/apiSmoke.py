from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Count

from rest_framework.authentication import TokenAuthentication
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
import threading

from TestPlatform.common.api_response import JsonResponse
from TestPlatform.models import dicom_record, base_data,smoke
from TestPlatform.serializers import dicomrecord_Serializer,dicomrecord_Deserializer,smoke_Deserializer,smoke_Serializer
from ..tools.smoke.gold import *
from ..tools.orthanc.deletepatients import *
from ..tools.dicom.duration_verify import *
from ..tools.stress.PerformanceResult import *
from ..common.stressfigure import *

logger = logging.getLogger(__name__)  # 这里使用 __name__ 动态搜索定义的 logger 配置


class getSmoke(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def get(self, request):
        """
        获取smoke数据
        :param request:
        :return:
        """
        try:
            page_size = int(request.GET.get("page_size", 20))
            page = int(request.GET.get("page", 1))
        except (TypeError, ValueError):
            return JsonResponse(code="999985", msg="page and page_size must be integer!")
        version = request.GET.get("version")

        if version:
            obi = smoke.objects.filter(version=version).order_by("version")
        else:
            obi = smoke.objects.all().order_by("-id")
        paginator = Paginator(obi, page_size)  # paginator对象
        total = paginator.num_pages  # 总页数
        try:
            obm = paginator.page(page)
        except PageNotAnInteger:
            obm = paginator.page(1)
        except EmptyPage:
            obm = paginator.page(paginator.num_pages)
        model =''
        serialize = smoke_Serializer(obm, many=True)
        for i in serialize.data:
            try:
                count = dicom_record.objects.filter(hostid=i['id']).aggregate(report_nums=Count("report"))
                success = dicom_record.objects.filter(hostid=i['id'], report='匹配成功').aggregate(report_nums=Count("report"))
                fail = dicom_record.objects.filter(hostid=i['id'], report='匹配失败').aggregate(report_nums=Count("report"))
                # id 转换成病种文案
                for j in i["diseases"].split(","):
                    obj = base_data.objects.get(id=j)
                    model = model + obj.remarks + ","
                i["diseases"] = model
                i["progress"] = '%.2f' % (int(i["progress"])/ int(i["count"]) * 100)
                i["success"] = success["report_nums"]
                i["fail"] = fail['report_nums']
                i["aifail"] = int(count['report_nums']) - int(success["report_nums"]) - int(fail['report_nums'])
                hostobj = GlobalHost.objects.get(id=i["hostid"])
                i["hostid"] = hostobj.host
            except Exception as e:
                i["host"] = "Null"
                continue
        return JsonResponse(data={"data": serialize.data,
                                  "page": page,
                                  "total": total
                                  }, code="0", msg="成功")



class AddSmoke(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def parameter_check(self, data):
        """
        验证参数
        :param data:
        :return:
        """
        try:
            # 必传参数 name, version, type
            if not data["hostid"] or not data["version"]:
                return JsonResponse(code="999996", msg="参数有误！")

        except KeyError:
            return JsonResponse(code="999996", msg="参数有误！")

    def post(self, request):
        """
        新增基础数据
        :param request:
        :return:
        """
        data = JSONParser().parse(request)
        result = self.parameter_check(data)
        if result:
            return result
        try:
            count = 0
            for i in data["diseases"]:
                obj = dicom.objects.filter(fileid=i)
                count = count + int(obj.count())
            data["diseases"] = str(data["diseases"])[1:-1]
            data["count"] = count
            smokeadd = smoke_Serializer(data=data)

            with transaction.atomic():
                smokeadd.is_valid()
                smokeadd.save()
            return JsonResponse(code="0", msg="成功")
        except Exception as e:
            return JsonResponse(code="999995", msg="{0}".format(e))

class UpdateSmoke(APIView):
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
            # 必传参数 content, predictor , type
            if not data["hostid"] or not data["version"]:
                return JsonResponse(code="999996", msg="参数有误 必传参数 content, predictor , type！")

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
            smokeobj = smoke.objects.get(id=data["id"])
        except Exception as e:
            return JsonResponse(code="999995", msg="数据不存在！")
        # 查找是否相同名称的项目
        name = smoke.objects.filter(version=data["version"]).exclude(id=data["id"])
        if len(name):
            return JsonResponse(code="999997", msg="存在相同内容数据")
        else:
            serializer = smoke_Deserializer(data=data)
            try:
                obj = dicom.objects.filter(fileid=data["id"])
                for i in obj:
                    i.diseases =data["remarks"]
                    i.save()
            except ObjectDoesNotExist:
                return JsonResponse(code="999998", msg="失败")
            with transaction.atomic():
                if serializer.is_valid():
                    # 修改数据
                    serializer.update(instance=baseobj, validated_data=data)
                    return JsonResponse(code="0", msg="成功")
                else:
                    return JsonResponse(code="999998", msg="失败")


class DelSmoke(APIView):
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
        删除信息
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
                    obj = smoke.objects.filter(id=j)
                    obj.delete()
                except Exception as e:
                    logger.error("删除smoke数据失败")
            return JsonResponse(code="0", msg="成功")
        except ObjectDoesNotExist:
            return JsonResponse(code="999995", msg="项目不存在！")


class DisableSmoke(APIView):
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
            obj = smoke.objects.get(id=data["id"])
            obj.status = False
            obj.save()
            return JsonResponse(code="0", msg="成功")
        except ObjectDoesNotExist:
            return JsonResponse(code="999995", msg="项目不存在！")


class EnableSmoke(APIView):
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
            obj = smoke.objects.get(id=data["id"])
            obj.status = True
            obj.save()

            return JsonResponse(code="0", msg="成功")
        except ObjectDoesNotExist:
            return JsonResponse(code="999995", msg="项目不存在！")

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
        diseases = request.GET.get("diseases")
        smokeid = request.GET.get("smokeid")

        if  request.GET.get("status")=='true':
            status = 1
        elif request.GET.get("status")=='False':
            status = 0
        else:
            status = ''

        if diseases != '' and status != '':
            obi = dicom_record.objects.filter(diseases__contains=diseases, status=status, hostid=smokeid).order_by("-id")
        elif diseases == ''  and status != '':
            obi = dicom_record.objects.filter(diseases__contains=diseases,status=status,hostid=smokeid).order_by("-id")
        else:
            obi = dicom_record.objects.filter(hostid=smokeid).order_by("-id")
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
            # 必传参数 server,version
            if not data["id"]:
                return JsonResponse(code="999996", msg="缺失必要参数,参数 id！")

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
            # 执行smoke测试
            try:
                thread_fake_folder = threading.Thread(target=goldSmoke,
                                                      args=(str(data["id"])))
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
            if not data["version"]:
                return JsonResponse(code="999996", msg="缺失必要参数,参数 version！")

        except KeyError:
            return JsonResponse(code="999996", msg="参数有误！")

    def post(self, request):
        """
        预测时间 金标准结果
        :param request:
        :return:
        """
        data = JSONParser().parse(request)
        result = self.parameter_check(data)
        if result:
            return result
        try:
            goldrows = []
            goldcolumns =[]
            # if data['version']:
            #     print(1)
            versions = smoke.objects.filter(status=True)
            for i in versions:
                goldcolumns.append(i.version)
                count = dicom_record.objects.filter(hostid=i.id).aggregate(report_nums=Count("report"))
                success = dicom_record.objects.filter(hostid=i.id,report='匹配成功').aggregate(report_nums=Count("report"))
                fail = dicom_record.objects.filter(hostid=i.id, report='匹配失败').aggregate(report_nums=Count("report"))
                histogram = {
                    '版本': i.version,
                    '匹配成功': success["report_nums"],
                    '匹配失败': fail['report_nums'],
                    '预测失败': int(count['report_nums']) - int(success["report_nums"]) - int(fail['report_nums'])
                }
                goldrows.append(histogram)
            return JsonResponse(data={"goldrows":goldrows,
                                      "goldcolumns":goldcolumns
                                      }, code="0", msg="成功")
        except Exception as e:
            return JsonResponse(msg="失败", code="999991", exception=e)
