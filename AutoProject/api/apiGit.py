from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.conf import settings
from django.db import transaction

from rest_framework.authentication import TokenAuthentication
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView

from AutoProject.common.api_response import JsonResponse
from AutoProject.serializers import project_git_Serializer
from ..common.install import InstallThread
from ..common.installReport import InstallReportThread
from AutoDicom.common.deletepatients import *
from ..models import install, Server, project_git
from ..common.Journal import readJournal
from ..common.biomind import Restart, createUser
from AutoInterface.models import gold_record
from ..common.GitApi import GitMethod

logger = logging.getLogger(__name__)  # 这里使用 __name__ 动态搜索定义的 logger 配置


class getGitBranch(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def get(self, request):
        """
        获取 项目 分支信息 版本
        :param request:
        :return:
        """
        try:
            children = []
            groupOptions = []
            project_id = request.GET.get("project_id", 1)
            try:
                Obj = project_git.objects.filter(status=True, Project_id=project_id).order_by("-id")
                for i in Obj:
                    Branch = GitMethod().gitBranch(i.gitname)
                    for j in Branch:
                        children.append(
                            {
                                "value": j,
                                "label": j
                            }
                        )

                    groupOptions.append({
                        "value": i.name,
                        "label": i.name,
                        "children": children
                    })
            except Exception as e:
                logger.error("查询报错：{}".format(e))
            return JsonResponse(data={"groupOptions": groupOptions}, code="0", msg="成功")
        except (TypeError, ValueError):
            return JsonResponse(code="999985", msg="获取版本失败!")


class getProjectGit(APIView):
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
        name = request.GET.get("name")

        if name:
            obi = project_git.objects.filter(name=name).order_by("-id")
        else:
            obi = project_git.objects.all().order_by("-id")
        paginator = Paginator(obi, page_size)  # paginator对象
        total = paginator.num_pages  # 总页数
        try:
            obm = paginator.page(page)
        except PageNotAnInteger:
            obm = paginator.page(1)
        except EmptyPage:
            obm = paginator.page(paginator.num_pages)
        serialize = project_git_Serializer(obm, many=True)

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
            journal, installStr, restartStr = readJournal(obj.Host.host, "Installation{}".format(data["id"]),
                                                          obj.Host.pwd)
        except (TypeError, ValueError):
            return JsonResponse(code="999985", msg="获取数据失败!", data="")
        return JsonResponse(data={"deploy": journal,
                                  "install": installStr,
                                  "restart": restartStr,
                                  "gold": "------暂未开放-------",
                                  }, code="0", msg="成功")
