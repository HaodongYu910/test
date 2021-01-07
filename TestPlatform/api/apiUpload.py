from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from rest_framework.authentication import TokenAuthentication
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from TestPlatform.common.api_response import JsonResponse
from ..models import uploadfile
from ..tools.stress.PerformanceResult import *


logger = logging.getLogger(__name__)  # 这里使用 __name__ 动态搜索定义的 logger 配置


class AddUpload(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def post(self, request):
        """
        上传文件
        :param request:
        :return:
        """
        try:
            filetype = request.POST.get("type", None)
            file_path = '/files1/files/{0}'.format(filetype)
            if not os.path.exists(file_path):
                os.makedirs(file_path)
            File = request.FILES.get("file", None)

            with open("{0}/{1}".format(file_path,File.name) , 'wb+') as f:
                # 分块写入文件
                for chunk in File.chunks():
                    f.write(chunk)

            data={
                "filename": File.name,
                "fileurl": file_path,
                "type": filetype,
                "status": True
            }
            filedata = uploadfile.objects.create(**data)
            return JsonResponse(code="0", msg="成功",data={"filename":File.name,"fileid": filedata.id}
                                )
        except ObjectDoesNotExist:
            return JsonResponse(code="999995", msg="没有需要上传的文件！")


class DelUpload(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def post(self, request):
        """
        删除上传文件
        :param request:
        :return:
        """
        try:
            data = JSONParser().parse(request)
            obj = uploadfile.objects.get(id=data["id"])
            obj.delete()
            file_name = "{0}/{2}".format(obj.fileurl,obj.filename)
            os.remove(file_name)
            return JsonResponse(code="0", msg="删除成功")
        except ObjectDoesNotExist:
            return JsonResponse(code="999995", msg="没有需要上传的文件！")
