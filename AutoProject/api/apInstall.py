from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.conf import settings
from django.db import transaction

from rest_framework.authentication import TokenAuthentication
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView

from AutoProject.common.api_response import JsonResponse
from AutoProject.serializers import install_Deserializer
from ..common.install import InstallThread
from ..common.installReport import InstallReportThread
from AutoDicom.common.deletepatients import *
from ..models import install, Server ,project_version
from ..common.Journal import readJournal
from ..common.biomind import Restart, createUser
from AutoInterface.models import gold_record
from ..common.frontend import frontend
logger = logging.getLogger(__name__)  # 这里使用 __name__ 动态搜索定义的 logger 配置


class InstallDeploy(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def post(self, request):
        """
        自动部署
        :param request:
        :return:
        user
        """

        data = JSONParser().parse(request)
        try:
            logger.info("InstallDeploy：{}".format(data))
            frontend(version=data["version"],
                     host=data["server"])
            return JsonResponse(code="0", msg="成功")
        except Exception as e:
            return JsonResponse(code="999995", msg="{0}".format(e))


class getInstallVersion(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def get(self, request):
        """
        获取Install 版本
        :param request:
        :return:
        """
        try:
            groupChildren = {}
            groupOptions = []
            try:
                Obj = project_version.objects.all().order_by("-id")
                for i in Obj:
                    if groupChildren.__contains__(i.branch) is False:
                        children = {
                            "value": i.id,
                            "label": i.package_name[:-4]
                        }
                        groupChildren[i.branch] = [children]
                    else:
                        groupChildren[i.branch].append({
                            "value": i.id,
                            "label": i.package_name[:-4]
                        })
            except Exception as e:
                logger.error("查询dicom文件报错：{}".format(e))

            for k, v in groupChildren.items():
                groupOptions.append({
                    "value": k,
                    "label": k,
                    "children": v
                })

            return JsonResponse(data={"groupOptions": groupOptions}, code="0", msg="成功")
        except (TypeError, ValueError):
            return JsonResponse(code="999985", msg="获取版本失败!")


class getInstall(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def get(self, request):
        """
        获取Install数据
        :param request:
        :return:
        """
        try:
            page_size = int(request.GET.get("page_size", 5))
            page = int(request.GET.get("page", 1))
        except (TypeError, ValueError):
            return JsonResponse(code="999985", msg="page and page_size must be integer!")
        version = request.GET.get("version")

        if version:
            obi = install.objects.filter(version=version).order_by("version")
        else:
            obi = install.objects.all().order_by("-id")
        paginator = Paginator(obi, page_size)  # paginator对象
        total = paginator.num_pages  # 总页数
        try:
            obm = paginator.page(page)
        except PageNotAnInteger:
            obm = paginator.page(1)
        except EmptyPage:
            obm = paginator.page(paginator.num_pages)
        serialize = install_Deserializer(obm, many=True)
        for i in serialize.data:
            i["version"] = project_version.objects.get(id=i["version"]).package_name[:-4]
            if i["status"] is True:
                # try:
                #     testThread = InstallThread(id=i["id"])
                #     i["cleantime"], i["uptime"], i["restarttime"] = testThread.getParm()
                # except:
                i["cleantime"], i["uptime"], i["restarttime"] = "", "", ""
            elif i["smokeid"] is not None:
                goldObj = gold_record.objects.filter(gold_id=i["smokeid"])
                i["progress"] = '%.2f' % (int(goldObj.count()) / int(121) * 100)

        return JsonResponse(data={"data": serialize.data,
                                  "page": page,
                                  "total": total
                                  }, code="0", msg="成功")

class getJournal(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def post(self, request):
        """
        获取Install 版本
        :param request:
        :return:
        """
        try:
            data = JSONParser().parse(request)
            obj = install.objects.get(id=data["id"])
            journal, installStr, restartStr = readJournal(obj.Host.host, "Installation{}".format(data["id"]), obj.Host.pwd)
        except (TypeError, ValueError):
            return JsonResponse(code="999985", msg="获取数据失败!", data="")
        return JsonResponse(data={"deploy": journal,
                                  "install": installStr,
                                  "restart": restartStr,
                                  "gold": "------暂未开放-------",
                                  }, code="0", msg="成功")

class getRestart(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def post(self, request):
        """
        重启& 创建用户
        :param request:
        :return:
        """
        try:
            data = JSONParser().parse(request)

            obj = install.objects.get(id=data["id"])
            if data["type"] == 1:
                Restart(id=obj.Host_id)
            else:
                createUser(user=data["user"], pwd=data["pwd"], protocol=obj.Host.protocol, server=obj.Host.host)
        except (TypeError, ValueError):
            return JsonResponse(code="999985", msg="重启失败!")
        return JsonResponse(code="0", msg="成功")

class AnsibleInstall(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def parameter_check(self, data):
        """
        验证参数
        :param data:
        :return:
        """
        try:
            # 必传参数 server
            if not data["tag_version"]:
                return JsonResponse(code="999996", msg="参数有误！")

        except KeyError:
            return JsonResponse(code="999996", msg="参数有误！")

    def post(self, request):
        """
        Ansible 安装版本
        :param request:
        :return:
        """
        data = JSONParser().parse(request)
        result = self.parameter_check(data)
        if result:
            return result
        try:
            obj = dictionary.objects.get(key=data["tag_version"], type='history', status=True)
            obj.status = False
            obj.save()
        except ObjectDoesNotExist:
            logger.info("Ansible 版本:{}".format(data))
        try:
            dictionary.objects.create(**{
                "key": data["tag_version"],
                "value": data["model_version"],
                "type": 'history',
                'status': True
            })
            return JsonResponse(code="0", msg="成功")
        except Exception as e:
            return JsonResponse(code="999995", msg="{0}".format(e))

class AddInstall(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def parameter_check(self, data):
        """
        验证参数
        :param data:
        :return:
        """
        try:
            # 必传参数 server
            if not data["Host"]:
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
            obj = Server.objects.get(id=data["Host"])
            data["version"] = str(data["version"][1])
            data["server"] = obj.host
            data["smokeid"] = 0 if data["smokeid"] is True else None
            data["uid"] = 0 if data["uid"] is True else None
            Installadd = install_Deserializer(data=data)

            with transaction.atomic():
                Installadd.is_valid()
                Installadd.save()
            return JsonResponse(code="0", msg="成功")
        except Exception as e:
            return JsonResponse(code="999995", msg="{0}".format(e))


class UpdateInstall(APIView):
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
            if not isinstance(data["Host_id"], int):
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
        try:
            Installobj = install.objects.get(id=data["id"])
        except Exception as e:
            return JsonResponse(code="999995", msg="数据不存在！")

        serializer = install_Deserializer(data=data)
        with transaction.atomic():
            if serializer.is_valid():
                # 修改数据
                serializer.update(instance=Installobj, validated_data=data)
                return JsonResponse(code="0", msg="成功")
            else:
                return JsonResponse(code="999998", msg="失败")


class DelInstall(APIView):
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
                    install.objects.filter(id=j).delete()
                except Exception as e:
                    logger.error("删除Install数据失败")
            return JsonResponse(code="0", msg="成功")
        except ObjectDoesNotExist:
            return JsonResponse(code="999995", msg="项目不存在！")


class DisableInstall(APIView):
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
            obj = install.objects.get(id=data["id"])
            obj.status = False
            obj.save()
            testThread = InstallThread(id=data["id"])
            # 设为保护线程，主进程结束会关闭线程
            testThread.setFlag = False

            return JsonResponse(code="0", msg="成功")
        except ObjectDoesNotExist:
            return JsonResponse(code="999995", msg="数据不存在！")


class EnableInstall(APIView):
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
            testThread = InstallThread(id=data["id"])
            testThread.setDaemon(True)
            # 开始线程
            testThread.start()

            return JsonResponse(code="0", msg="成功")
        except ObjectDoesNotExist:
            return JsonResponse(code="999995", msg="项目不存在！")


class getInstallReport(APIView):
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
            if not data["id"]:
                return JsonResponse(code="999996", msg="参数有误！")
        except KeyError:
            return JsonResponse(code="999996", msg="参数有误！")

    def post(self, request):
        """
        冒烟测试报告
        :param request:
        :return:
        """
        data = JSONParser().parse(request)
        result = self.parameter_check(data)
        if result:
            return result
        # 查找是否存在
        try:
            testThread = InstallReportThread(id=data["id"])
            data = testThread.report()
            return JsonResponse(code="0", msg="成功", data=data)

        except ObjectDoesNotExist:
            return JsonResponse(code="999995", msg="数据不存在！")


class InstallSmoke(APIView):
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
            if not data["id"]:
                return JsonResponse(code="999996", msg="参数有误！")
        except KeyError:
            return JsonResponse(code="999996", msg="参数有误！")

    def post(self, request):
        """
        冒烟测试 对外接口
        :param request:
        :return:
        """
        data = JSONParser().parse(request)
        result = self.parameter_check(data)
        if result:
            return result
        # 查找是否存在
        try:
            InSmoke = InGoldThread(id=data["id"])
            InSmoke.setDaemon(True)
            # 开始线程
            InSmoke.start()
            return JsonResponse(code="0", msg="成功", data=data)

        except ObjectDoesNotExist:
            return JsonResponse(code="999995", msg="数据不存在！")