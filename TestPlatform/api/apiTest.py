from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db import transaction
from django.db.models import Count

from rest_framework.authentication import TokenAuthentication
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
import threading

from TestPlatform.common.api_response import JsonResponse
from TestPlatform.serializers import autotest_Serializer,autotest_Deserializer,autocase_Serializer,autorecord_Serializer,autorecord_Deserializer
from ..tools.orthanc.deletepatients import *
from ..models import autotest,auto_record,auto_case,uploadfile
logger = logging.getLogger(__name__)  # 这里使用 __name__ 动态搜索定义的 logger 配置

class getAutoCase(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def get(self, request):
        """
        获取用例
        :param request:
        :return:
        """
        try:
            page_size = int(request.GET.get("page_size", 20))
            page = int(request.GET.get("page", 1))
            type = request.GET.get("type")
            name = request.GET.get("name")
        except (TypeError, ValueError):
            return JsonResponse(code="999985", msg="page and page_size must be integer!")
        if name:
            obi = auto_case.objects.filter(name=name).order_by("id")
        elif type:
            obi = auto_case.objects.filter(type=type).order_by("id")
        else:
            obi = auto_case.objects.all().order_by("-id")
        paginator = Paginator(obi, page_size)  # paginator对象
        total = paginator.num_pages  # 总页数
        try:
            obm = paginator.page(page)
        except PageNotAnInteger:
            obm = paginator.page(1)
        except EmptyPage:
            obm = paginator.page(paginator.num_pages)
        serialize = autocase_Serializer(obm, many=True)
        # for i in serialize.data:
        #     model = ''
        #     try:
        #         # count = auto_record.objects.filter(smokeid=i['id']).aggregate(result_nums=Count("result"))
        #         # success = auto_record.objects.filter(smokeid=i['id'], result='匹配成功').aggregate(result_nums=Count("result"))
        #         # fail = auto_record.objects.filter(smokeid=i['id'], result='匹配失败').aggregate(result_nums=Count("result"))
        #         # id 转换成病种文案
        #         # for j in i["diseases"].split(","):
        #         #     obj = base_data.objects.get(id=j)
        #         #     model = model + obj.remarks + ","
        #         # i["diseases"] = model
        #         i["progress"] = '%.2f' % (int(i["progress"])/ int(i["count"]) * 100)
        #         # i["success"] = success["result_nums"]
        #         # i["fail"] = fail['result_nums']
        #         # i["aifail"] = int(count['result_nums']) - int(success["result_nums"]) - int(fail['result_nums'])
        #         hostobj = GlobalHost.objects.get(id=i["hostid"])
        #         i["hostid"] = hostobj.host
        #     except Exception as e:
        #         i["host"] = "Null"
        #         continue
        return JsonResponse(data={"data": serialize.data,
                                  "page": page,
                                  "total": total
                                  }, code="0", msg="成功")

class AddAutoCase(APIView):
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
            if not data["type"] or not data["name"]:
                return JsonResponse(code="999996", msg="参数有误！")

        except KeyError:
            return JsonResponse(code="999996", msg="参数有误！")

    def post(self, request):
        """
        新增用例
        :param request:
        :return:
        """
        data = JSONParser().parse(request)
        result = self.parameter_check(data)
        if result:
            return result
        try:
            data["testdata"] = str(data["testdata"])[1:-1]
            dict = data['filedict']
            autoadd = autocase_Serializer(data=data)

            with transaction.atomic():
                autoadd.is_valid()
                acase=autoadd.save()
            if dict != {}:
                for k, v in dict.items():
                    try:
                        obj = uploadfile.objects.get(id=v)
                        obj.fileid = str(acase.id)
                        obj.save()
                    except Exception as e:
                        logger.error("更新upload数据失败{0},错误：{1}".format(v, e))
                        continue
            return JsonResponse(code="0", msg="成功")
        except Exception as e:
            return JsonResponse(code="999995", msg="{0}".format(e))

class UpdateAutoCase(APIView):
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
            if not data["id"] or not data["version"]:
                return JsonResponse(code="999996", msg="参数有误 必传参数 content, predictor , type！")

        except KeyError:
            return JsonResponse(code="999996", msg="参数有误！")

    def post(self, request):
        """
        修改用例
        :param request:
        :return:
        """
        data = JSONParser().parse(request)
        result = self.parameter_check(data)
        if result:
            return result
        #
        try:
            autoobj = auto_case.objects.get(id=data["id"])
        except Exception as e:
            return JsonResponse(code="999995", msg="数据不存在！")
        # 查找是否相同名称的项目
        name = autotest.objects.filter(name=data["name"]).exclude(id=data["id"])
        if len(name):
            return JsonResponse(code="999997", msg="存在相同内容数据")
        else:
            serializer = autotest_Deserializer(data=data)
            with transaction.atomic():
                if serializer.is_valid():
                    # 修改数据
                    serializer.update(instance=autoobj, validated_data=data)
                    if dict != {}:
                        for k, v in dict.items():
                            try:
                                obj = uploadfile.objects.get(id=v)
                                obj.fileid = str(data["id"])
                                obj.save()
                            except Exception as e:
                                logger.error("更新upload数据失败{0},错误：{1}".format(v, e))
                                continue
                    return JsonResponse(code="0", msg="成功")
                else:
                    return JsonResponse(code="999998", msg="失败")


class DelAutoCase(APIView):
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
                    obj = auto_case.objects.filter(id=j)
                    obj.delete()
                except Exception as e:
                    logger.error("删除smoke数据失败")
            return JsonResponse(code="0", msg="成功")
        except ObjectDoesNotExist:
            return JsonResponse(code="999995", msg="项目不存在！")


class DisableAutoCase(APIView):
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
            obj = auto_case.objects.get(id=data["id"])
            obj.status = False
            obj.save()
            return JsonResponse(code="0", msg="成功")
        except ObjectDoesNotExist:
            return JsonResponse(code="999995", msg="项目不存在！")


class EnableAutoCase(APIView):
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
            obj = auto_case.objects.get(id=data["id"])
            obj.status = True
            obj.save()

            return JsonResponse(code="0", msg="成功")
        except ObjectDoesNotExist:
            return JsonResponse(code="999995", msg="项目不存在！")

class getAutoTest(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def get(self, request):
        """
        获取AutoTest数据
        :param request:
        :return:
        """
        try:
            page_size = int(request.GET.get("page_size", 20))
            page = int(request.GET.get("page", 1))
            version = request.GET.get("version")
            type =request.GET.get("type")
        except (TypeError, ValueError):
            return JsonResponse(code="999985", msg="page and page_size must be integer!")

        if version:
            obi = autotest.objects.filter(version=version,type=type).order_by("version")
        elif type:
            obi = autotest.objects.filter(type=type).order_by("version")
        else:
            obi = autotest.objects.all().order_by("-id")
        paginator = Paginator(obi, page_size)  # paginator对象
        total = paginator.num_pages  # 总页数
        try:
            obm = paginator.page(page)
        except PageNotAnInteger:
            obm = paginator.page(1)
        except EmptyPage:
            obm = paginator.page(paginator.num_pages)
        serialize = autotest_Serializer(obm, many=True)
        for i in serialize.data:
            try:
                # count = auto_record.objects.filter(smokeid=i['id']).aggregate(result_nums=Count("result"))
                # success = auto_record.objects.filter(smokeid=i['id'], result='匹配成功').aggregate(result_nums=Count("result"))
                # fail = auto_record.objects.filter(smokeid=i['id'], result='匹配失败').aggregate(result_nums=Count("result"))
                # id 转换成病种文案
                # for j in i["diseases"].split(","):
                #     obj = base_data.objects.get(id=j)
                #     model = model + obj.remarks + ","
                # i["diseases"] = model
                i["progress"] = '%.2f' % (int(i["progress"]) * 100)
                # i["success"] = success["result_nums"]
                # i["fail"] = fail['result_nums']
                # i["aifail"] = int(count['result_nums']) - int(success["result_nums"]) - int(fail['result_nums'])
                hostobj = GlobalHost.objects.get(id=i["hostid"])
                i["hostid"] = hostobj.host
            except Exception as e:
                i["host"] = "Null"
                continue
        return JsonResponse(data={"data": serialize.data,
                                  "page": page,
                                  "total": total
                                  }, code="0", msg="成功")



class AddAutoTest(APIView):
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
        新增自动测试
        :param request:
        :return:
        """
        data = JSONParser().parse(request)
        result = self.parameter_check(data)
        if result:
            return result
        try:
            data["setup"] = str(data["setup"])[1:-1]
            data["cases"] = str(data["cases"])[1:-1]
            data["tearDown"] = str(data["tearDown"])[1:-1]
            autoadd = autotest_Serializer(data=data)

            with transaction.atomic():
                autoadd.is_valid()
                autoadd.save()
            return JsonResponse(code="0", msg="成功")
        except Exception as e:
            return JsonResponse(code="999995", msg="{0}".format(e))

class UpdateAutoTest(APIView):
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
            if not isinstance(data["hostid"], int):
                return JsonResponse(code="999996", msg="参数有误！")
            # 必传参数 content, predictor , type
            if not data["id"] or not data["version"]:
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
            autoobj = autotest.objects.get(id=data["id"])
        except Exception as e:
            return JsonResponse(code="999995", msg="数据不存在！")
        # 查找是否相同名称的项目
        name = autotest.objects.filter(version=data["version"]).exclude(id=data["id"])
        if len(name):
            return JsonResponse(code="999997", msg="存在相同内容数据")
        else:
            serializer = autotest_Deserializer(data=data)
            try:
                obj = dicom.objects.filter(fileid=data["id"])
                for i in obj:
                    i.diseases = data["remarks"]
                    i.save()
            except ObjectDoesNotExist:
                return JsonResponse(code="999998", msg="失败")
            with transaction.atomic():
                if serializer.is_valid():
                    # 修改数据
                    serializer.update(instance=autoobj, validated_data=data)
                    return JsonResponse(code="0", msg="成功")
                else:
                    return JsonResponse(code="999998", msg="失败")


class DelAutoTest(APIView):
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
                    obj = autotest.objects.filter(id=j)
                    obj.delete()
                except Exception as e:
                    logger.error("删除smoke数据失败")
            return JsonResponse(code="0", msg="成功")
        except ObjectDoesNotExist:
            return JsonResponse(code="999995", msg="项目不存在！")


class DisableAutoTest(APIView):
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
            obj = autotest.objects.get(id=data["id"])
            obj.status = False
            obj.save()
            return JsonResponse(code="0", msg="成功")
        except ObjectDoesNotExist:
            return JsonResponse(code="999995", msg="项目不存在！")


class EnableAutoTest(APIView):
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
            obj = autotest.objects.get(id=data["id"])
            obj.status = True
            obj.save()

            return JsonResponse(code="0", msg="成功")
        except ObjectDoesNotExist:
            return JsonResponse(code="999995", msg="项目不存在！")

class AutoRecord(APIView):
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
            obi = auto_record.objects.filter(diseases__contains=diseases, status=status, smokeid=smokeid).order_by("-id")
        elif diseases == ''  and status != '':
            obi = auto_record.objects.filter(diseases__contains=diseases,status=status,smokeid=smokeid).order_by("-id")
        else:
            obi = auto_record.objects.filter(smokeid=smokeid).order_by("-id")
        paginator = Paginator(obi, page_size)  # paginator对象
        total = paginator.num_pages  # 总页数
        try:
            obm = paginator.page(page)
        except PageNotAnInteger:
            obm = paginator.page(1)
        except EmptyPage:
            obm = paginator.page(paginator.num_pages)
        serialize = autorecord_Serializer(obm, many=True)
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


class AutoTest(APIView):
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
                obj = auto_record.objects.filter(smokeid=str(data["id"]))
                obj.delete()
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


class getCaseFile(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def get(self, request):
        """
        获取用例内容
        :param request:
        :return:
        """
        try:
            id = int(request.GET.get("id", 20))
            obj = uploadfile.objects.get(fileid=id)
            with open('{0}/{1}'.format(obj.fileurl,obj.filename), 'r', encoding='utf-8') as f:
                data = f.read()
                f.close()
        except (TypeError, ValueError):
            return JsonResponse(code="999985", msg="page and page_size must be integer!")

        return JsonResponse(data={"data": data
                                  }, code="0", msg="成功")

class UpdateCaseFile(APIView):
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
            if not data["type"] or not data["name"]:
                return JsonResponse(code="999996", msg="参数有误！")

        except KeyError:
            return JsonResponse(code="999996", msg="参数有误！")

    def post(self, request):
        """
        新增用例
        :param request:
        :return:
        """
        data = JSONParser().parse(request)
        result = self.parameter_check(data)
        if result:
            return result
        try:
            id = data["id"]
            obj = uploadfile.objects.get(fileid=id)
            f = open('{0}/{1}'.format(obj.fileurl, obj.filename), 'r', encoding='utf-8')
            data = f.read()
            f.close()
            return JsonResponse(code="0", msg="成功")
        except Exception as e:
            return JsonResponse(code="999995", msg="{0}".format(e))

class Autofigure(APIView):
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
            versions = autotest.objects.filter(status=True)
            for i in versions:
                goldcolumns.append(i.version)
                count = auto_record.objects.filter(smokeid=i.id).aggregate(report_nums=Count("report"))
                success = auto_record.objects.filter(smokeid=i.id,report='匹配成功').aggregate(report_nums=Count("report"))
                fail = auto_record.objects.filter(smokeid=i.id, report='匹配失败').aggregate(report_nums=Count("report"))
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
