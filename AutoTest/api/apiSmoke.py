from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Count

from rest_framework.authentication import TokenAuthentication
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from django.db import transaction
from AutoTest.common.api_response import JsonResponse
from AutoTest.serializers import smoke_Deserializer, smoke_Serializer, smokerecord_Serializer
from AutoTest.common.gold import SmokeThread
from AutoDicom.common.deletepatients import *
from ..models import smoke_record,smoke
from AutoDicom.common.dicomBase import baseTransform
import time

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
        serialize = smoke_Serializer(obm, many=True)
        for i in serialize.data:
            try:
                count = smoke_record.objects.filter(smokeid=i['id']).aggregate(result_nums=Count("result"))
                success = smoke_record.objects.filter(smokeid=i['id'], result='匹配成功').aggregate(
                    result_nums=Count("result"))
                fail = smoke_record.objects.filter(smokeid=i['id'], result='匹配失败').aggregate(
                    result_nums=Count("result"))
                i["diseases"] = baseTransform(i["diseases"], 'base')
                i["progress"] = '%.2f' % (int(i["progress"]) / int(i["count"]) * 100)
                i["success"] = success["result_nums"]
                i["fail"] = fail['result_nums']
                i["aifail"] = int(count['result_nums']) - int(success["result_nums"]) - int(fail['result_nums'])
                hostobj = Server.objects.get(id=i["Host"])
                i["Host"] = hostobj.host
            except Exception as e:
                i["Host"] = "Null"
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
            # 必传参数 Host, version
            if not data["Host"] or not data["version"]:
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
            obj = dicom.objects.filter(fileid__in=data["diseases"])
            data["count"] = int(obj.count())
            data["diseases"] = str(data["diseases"])[1:-1]
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
            # # 校验Host 类型为int
            # if not isinstance(data["Host"], int):
            #     return JsonResponse(code="999996", msg="参数有误！")
            # 必传参数 id, version
            if not data["id"] or not data["version"]:
                return JsonResponse(code="999996", msg="参数有误 必传参数 id, version ！")

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
        obj = dicom.objects.filter(fileid__in=data["diseases"])
        data["count"] = int(obj.count())
        data["diseases"] = str(data["diseases"])[1:-1]
        try:
            smokeobj = smoke.objects.get(id=data["id"])
        except Exception as e:
            return JsonResponse(code="999995", msg="数据不存在：{}！".format(e))

        serializer = smoke_Deserializer(data=data)
        with transaction.atomic():
            if serializer.is_valid():
                # 修改数据
                serializer.update(instance=smokeobj, validated_data=data)
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
            testThread = SmokeThread(data["id"])
            # 设为保护线程，主进程结束会关闭线程
            testThread.setFlag = False

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
            objrecord = smoke_record.objects.filter(smokeid=str(data["id"]))
            # 删除以前记录
            objrecord.delete()

            testThread = SmokeThread(data["id"])
            # 设为保护线程，主进程结束会关闭线程
            testThread.setDaemon(True)
            # 开始线程
            testThread.start()

            # 变更状态
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
        status = request.GET.get("status")

        if diseases != '' and status != '':
            if status in ["0","1"]:
                obi = smoke_record.objects.filter(diseases=diseases, status=int(status), smokeid=smokeid).order_by(
                    "-id")
            else:
                obi = smoke_record.objects.filter(diseases=diseases, result=status, smokeid=smokeid).order_by(
                    "-id")
        elif diseases == '' and status != '':
            if status in ["0","1"]:
                obi = smoke_record.objects.filter(status=int(status), smokeid=smokeid).order_by(
                    "-id")
            else:
                obi = smoke_record.objects.filter(result=status, smokeid=smokeid).order_by(
                    "-id")
        elif diseases != '' and status == '':
            obi = smoke_record.objects.filter(diseases=diseases, smokeid=smokeid).order_by(
                    "-id")
        else:
            obi = smoke_record.objects.filter(smokeid=smokeid).order_by("-id")
        paginator = Paginator(obi, page_size)  # paginator对象
        total = paginator.num_pages  # 总页数
        try:
            obm = paginator.page(page)
        except PageNotAnInteger:
            obm = paginator.page(1)
        except EmptyPage:
            obm = paginator.page(paginator.num_pages)
        serialize = smokerecord_Serializer(obm, many=True)
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
            goldcolumns = []
            # if data['version']:
            #     print(1)
            versions = smoke.objects.filter(status=True)
            for i in versions:
                goldcolumns.append(i.version)
                count = smoke_record.objects.filter(smokeid=i.id).aggregate(report_nums=Count("report"))
                success = smoke_record.objects.filter(smokeid=i.id, report='匹配成功').aggregate(
                    report_nums=Count("report"))
                fail = smoke_record.objects.filter(smokeid=i.id, report='匹配失败').aggregate(report_nums=Count("report"))
                histogram = {
                    '版本': i.version,
                    '匹配成功': success["report_nums"],
                    '匹配失败': fail['report_nums'],
                    '预测失败': int(count['report_nums']) - int(success["report_nums"]) - int(fail['report_nums'])
                }
                goldrows.append(histogram)
            return JsonResponse(data={"goldrows": goldrows,
                                      "goldcolumns": goldcolumns
                                      }, code="0", msg="成功")
        except Exception as e:
            return JsonResponse(msg="失败", code="999991", exception=e)
