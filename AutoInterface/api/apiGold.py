from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Count, When, Case
from django.db import transaction

from rest_framework.authentication import TokenAuthentication
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView

from AutoProject.common.api_response import JsonResponse
from AutoInterface.serializers import gold_Deserializer, gold_Serializer, gold_record_Serializer
from AutoInterface.common.gold import GoldThread
from AutoInterface.common.goldReport import GoldReportThread

from AutoDicom.common.dicomBase import baseTransform
from AutoDicom.common.deletepatients import *

from ..models import gold_record, gold_test
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
            obi = gold_test.objects.filter(version=version).order_by("version")
        else:
            obi = gold_test.objects.all().order_by("-id")
        paginator = Paginator(obi, page_size)  # paginator对象
        total = paginator.num_pages  # 总页数
        try:
            obm = paginator.page(page)
        except PageNotAnInteger:
            obm = paginator.page(1)
        except EmptyPage:
            obm = paginator.page(paginator.num_pages)
        serialize = gold_Serializer(obm, many=True)
        for i in serialize.data:
            try:
                i["Host"] = Server.objects.get(id=int(i["Host"])).host
                i["diseases"] = baseTransform(i["diseases"], 'base')
                smokeResult = gold_record.objects.filter(
                    gold_id=i["id"]).values('gold_id').annotate(
                    total=Count('gold_id'),
                    success=Count(Case(When(result='匹配成功', then=0))),
                    fail=Count(Case(When(result='匹配失败', then=0)))
                )
                i["progress"] = '%.2f' % (int(smokeResult[0]["total"]) / int(i["count"]) * 100)
                i["success"] = smokeResult[0]["success"]
                i["fail"] = smokeResult[0]["fail"]
                i["aifail"] = int(smokeResult[0]["total"]) - int(smokeResult[0]["success"]) - int(smokeResult[0]["fail"])
            except Exception as e:
                i["success"] = 0
                i["fail"] = 0
                i["aifail"] = 0
                i["progress"] = 0
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
            testdata = ''
            obj = dicom.objects.filter(fileid__in=data["diseases"], status=True)
            data["count"] = int(obj.count())
            # 循环保证 字符串中无空格
            for j in data["diseases"]:
                testdata = testdata + str(j) + ","
            data["diseases"] = testdata[:-1]
            smokeadd = gold_Serializer(data=data)

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
        testdata =""
        data = JSONParser().parse(request)
        result = self.parameter_check(data)
        if result:
            return result
        obj = dicom.objects.filter(fileid__in=data["diseases"], status=True)
        data["count"] = int(obj.count())
        # 循环保证 字符串中无空格
        for j in data["diseases"]:
            testdata = testdata + str(j) + ","
        data["diseases"] = testdata[:-1]
        try:
            smokeobj = gold_test.objects.get(id=data["id"])
        except Exception as e:
            return JsonResponse(code="999995", msg="数据不存在：{}！".format(e))

        serializer = gold_Deserializer(data=data)
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
                    obj = gold_test.objects.filter(id=j)
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
            obj = gold_test.objects.get(id=data["id"])
            obj.status = False
            obj.save()
            testThread = GoldThread(data["id"])
            # 设为保护线程，主进程结束会关闭线程
            testThread.setFlag = False
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
            obj = gold_test.objects.get(id=data["id"])
            objrecord = gold_record.objects.filter(gold_id=str(data["id"]))
            # 删除以前记录
            objrecord.delete()

            testThread = GoldThread(data["id"])
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
        gold_id = request.GET.get("gold_id")
        status = request.GET.get("status")

        if diseases != '' and status != '':
            if status in ["0","1"]:
                obi = gold_record.objects.filter(diseases=diseases, status=int(status), gold_id=gold_id).order_by(
                    "-id")
            else:
                obi = gold_record.objects.filter(diseases=diseases, result=status, gold_id=gold_id).order_by(
                    "-id")
        elif diseases == '' and status != '':
            if status in ["0","1"]:
                obi = gold_record.objects.filter(status=int(status), gold_id=gold_id).order_by(
                    "-id")
            else:
                obi = gold_record.objects.filter(result=status, gold_id=gold_id).order_by(
                    "-id")
        elif diseases != '' and status == '':
            obi = gold_record.objects.filter(diseases=diseases, gold_id=gold_id).order_by(
                    "-id")
        else:
            obi = gold_record.objects.filter(gold_id=gold_id).order_by("-id")
        paginator = Paginator(obi, page_size)  # paginator对象
        total = paginator.num_pages  # 总页数
        try:
            obm = paginator.page(page)
        except PageNotAnInteger:
            obm = paginator.page(1)
        except EmptyPage:
            obm = paginator.page(paginator.num_pages)
        serialize = gold_record_Serializer(obm, many=True)
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
            versions = gold_test.objects.filter(status=True)
            for i in versions:
                goldcolumns.append(i.version)
                count = gold_record.objects.filter(gold_id=i.id).aggregate(report_nums=Count("report"))
                success = gold_record.objects.filter(gold_id=i.id, report='匹配成功').aggregate(
                    report_nums=Count("report"))
                fail = gold_record.objects.filter(gold_id=i.id, report='匹配失败').aggregate(report_nums=Count("report"))
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


class getGoldReport(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def get(self, request):
        """
        冒烟测试报告
        :param request:
        :return:
        """
        try:
            goldid = int(request.GET.get("id"))
        except (TypeError, ValueError):
            return JsonResponse(code="999985", msg="goldid must be integer!")
        # 查找是否存在
        try:
            reportThread = GoldReportThread(goldid)
            data = reportThread.report()
            return JsonResponse(code="0", msg="成功", data=data)

        except ObjectDoesNotExist:
            return JsonResponse(code="999995", msg="数据不存在！")