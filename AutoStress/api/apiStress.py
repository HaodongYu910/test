from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db import transaction

from rest_framework.authentication import TokenAuthentication
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView

from AutoProject.common.api_response import JsonResponse
from ..serializers import stress_Deserializer, stress_result_Deserializer, stress_jmeter_Serializer

from AutoDicom.common.dicomBase import baseTransform
from AutoDicom.common.deletepatients import *

from ..common.manual import ManualThread
from ..common.stress import StressTest
from ..common.StrategyDetail import strategyList

from AutoProject.models import uploadfile, project_version

from ..models import stress, stress_record, stress_result
import os
import shutil
import datetime


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
                return JsonResponse(code="999996", msg="缺失必要参数,参数 ids！")

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
        stressId = data["stressid"]
        if result:
            return result
        try:
            st = StressTest(stressID=stressId, modelID=data['modelId'], Type=data['type'])
            st.setDaemon(True)
            st.start()

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
            # 必传参数 ids
            if not data["ids"]:
                return JsonResponse(code="999996", msg="缺失必要参数,参数 ids！")

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
            stressid = data["ids"][0]
            obj = stress.objects.get(stressid=stressid)
            obj.status = False
            obj.teststatus = '已停止'
            obj.save()
            if obj.teststatus == "基准测试":
                stop = ManualThread(stressid=stressid, modelID='')
            else:
                stop = StressTest(stressID=stressid, Type='')
            stop.stop = False
            # 删除文件夹
            try:
                folder = "/home/biomind/Biomind_Test_Platform/logs/ST{0}".format(str(obj.stressid))
                if os.path.exists(folder):
                    shutil.rmtree(folder)
            except Exception as e:
                logger.error("删除文件夹失败：{}".format(e))

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
            page_size = int(request.GET.get("page_size", 5))
            page = int(request.GET.get("page", 1))
            project_id = int(request.GET.get("project_id", 1))
        except (TypeError, ValueError):
            return JsonResponse(code="999985", msg="page and page_size must be integer!")
        version = request.GET.get("version")

        # 判断查询数据类型
        if version:
            obi = stress.objects.filter(version=version, status=True, project_id=project_id).order_by("-stressid")
        else:
            obi = stress.objects.filter(project_id=project_id).order_by("-stressid")
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
            try:
                i["version"] = project_version.objects.get(id=i["version"]).version
            except:
                continue
            i["testdata"] = baseTransform(i["testdata"], 'dictionary')
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

            for i in stressserializer.data:
                try:
                    i["version"] = project_version.objects.get(id=i["version"]).version
                except:
                    logger.error("version")

            return JsonResponse(data={"data": stressserializer.data
                                      }, code="0", msg="成功")
        except Exception as e:
            logger.error(e)
            return JsonResponse(msg="失败", code="999991", exception=e)


class strategyDetail(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def get(self, request):
        """
                获取压测详情
                :param request:
                :return:
                """
        try:
            stressId = request.GET.get("stressid")
            strategy = request.GET.get("strategy")
            data = strategyList(stressId=stressId, strategy=strategy)
            return JsonResponse(data=data, code="0", msg="成功")
        except Exception as e:
            logger.error(e)
            return JsonResponse(msg="失败", code="999991", exception=e)


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
            # 必传参数 testdata, Host , version
            if not data["testdata"] or not data["Host"] or not data["version"]:
                return JsonResponse(code="999996", msg="参数有误,必传参数 version, Host！")

        except KeyError:
            return JsonResponse(code="999996", msg="参数有误,必传参数 version, Host testdata！！")

    def post(self, request):
        """
        添加性能测试
        :param request:
        :return:
        """
        data = JSONParser().parse(request)
        result = self.parameter_check(data)
        if result:
            return result
        try:
            testdata = ''
            if data['uploadID']:
                data['jmeterstatus'] = True
            hostobj = Server.objects.get(id=data['Host'])
            data["loadserver"] = hostobj.host
            # 循环保证 字符串中无空格
            for j in data["testdata"]:
                testdata = testdata + str(j) + ","
            data["testdata"] = testdata[:-1]
            StressAdd = stress_Deserializer(data=data)

            with transaction.atomic():
                StressAdd.is_valid()
                stressID = StressAdd.save()
                try:
                    if data['uploadID']:
                        uploadObj = uploadfile.objects.get(id=data['uploadID'])
                        data["name"] = uploadObj.filename
                        data["route"] = f"{uploadObj.fileurl}/{uploadObj.filename}"
                        data["status"] = True
                        data["Stress"] = stressID.stressid
                        add = stress_jmeter_Serializer(data=data)
                        with transaction.atomic():
                            add.is_valid()
                            add.save()
                except Exception as e:
                    logger.error("{0}".format(e))

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
            # 必传参数 stressid
            if not data["stressid"]:
                return JsonResponse(code="999996", msg="参数有误,必传参数 id！")

        except KeyError:
            return JsonResponse(code="999996", msg="参数有误！")

    def post(self, request):
        """
        修改性能测试
        :param request:
        :return:
        """
        data = JSONParser().parse(request)
        result = self.parameter_check(data)
        if result:
            return result
        try:

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
            if not data["stressid"]:
                return JsonResponse(code="999996", msg="参数有误！")
        except KeyError:
            return JsonResponse(code="999996", msg="参数有误！")

    def post(self, request):
        """
        禁用性能
        :param request:
        :return:
        """
        data = JSONParser().parse(request)
        result = self.parameter_check(data)
        if result:
            return result
        # 查找是否存在
        try:
            stressid = data["stressid"]
            obj = stress.objects.get(stressid=stressid)
            obj.status = False
            obj.teststatus = '已停止'
            obj.save()
            if obj.teststatus == "基准测试":
                stoptest = ManualThread(stressid=stressid)
            else:
                # 删除文件夹
                try:
                    folder = "/home/biomind/Biomind_Test_Platform/logs/ST{0}".format(str(obj.stressid))
                    if os.path.exists(folder):
                        shutil.rmtree(folder)
                except Exception as e:
                    logger.error("删除文件夹失败：{}".format(e))

            return JsonResponse(code="0", msg="已停止")

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
            # 校验stressid
            if not data["stressid"]:
                return JsonResponse(code="999996", msg="参数有误！")
        except KeyError:
            return JsonResponse(code="999996", msg="参数有误！")

    def post(self, request):
        """
        启用性能
        :param request:
        :return:
        """
        data = JSONParser().parse(request)
        result = self.parameter_check(data)
        if result:
            return result
        # 查找是否存在
        try:
            st = StressTest(stressID=data["stressid"], Type=data["type"])
            st.setDaemon(True)
            st.start()

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
            # 校验stressid
            if not data["stressid"]:
                return JsonResponse(code="999996", msg="参数有误！")
        except KeyError:
            return JsonResponse(code="999996", msg="参数有误！")

    def post(self, request):
        """
        删除性能测试
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


