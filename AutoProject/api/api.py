
from rest_framework.authentication import TokenAuthentication
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from django.db import transaction
from AutoProject.common.api_response import JsonResponse
from AutoProject.serializers import install_Deserializer
from AutoProject.scheduletask import *
from AutoDicom.common.deletepatients import *
from AutoStress.models import stress_result
logger = logging.getLogger(__name__)  # 这里使用 __name__ 动态搜索定义的 logger 配置


class test(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def post(self, request):
        """
        test
        :param request:
        :return:
        """

        data = JSONParser().parse(request)
        try:
            obj = stress_result.objects.filter(type__in=["lung_JZ"])
            obb = stress_result.objects.filter(type__in=["lung_jobJZ"])
            for i in obj:
                for j in obb:
                    if i.version == j.version and i.modelname == j.modelname and i.slicenumber ==j.slicenumber:
                        i.type = 'JZ'
                        i.jobavg = j.avg
                        i.jobmedian = j.median
                        i.jobmin = j.min
                        i.jobmax = j.max
                        i.save()


            #NightlyReportTask()

            return JsonResponse(code="0", msg="成功")
        except Exception as e:
            return JsonResponse(code="999995", msg="{0}".format(e))

