from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from rest_framework.authentication import TokenAuthentication
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from AutoProject.common.api_response import JsonResponse
from ..models import uploadfile
from ..serializers import uploadfile_Deserializer
import logging,os
import zipfile

logger = logging.getLogger(__name__)  # 这里使用 __name__ 动态搜索定义的 logger 配置


class getUpload(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def get(self, request):
        """
        获取Upload数据
        :param request:
        :return:
        """
        try:
            page_size = int(request.GET.get("page_size", 20))
            page = int(request.GET.get("page", 1))
            type =request.GET.get("type")
        except (TypeError, ValueError):
            return JsonResponse(code="999985", msg="page and page_size must be integer!")
        version = request.GET.get("version")

        if version:
            obi = uploadfile.objects.filter(version=version,type=type).order_by("id")
        else:
            obi = uploadfile.objects.filter(type=type).order_by("-id")
        paginator = Paginator(obi, page_size)  # paginator对象
        total = paginator.num_pages  # 总页数
        try:
            obm = paginator.page(page)
        except PageNotAnInteger:
            obm = paginator.page(1)
        except EmptyPage:
            obm = paginator.page(paginator.num_pages)
        serialize = uploadfile_Deserializer(obm, many=True)
        return JsonResponse(data={"data": serialize.data,
                                  "page": page,
                                  "total": total
                                  }, code="0", msg="成功")

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

class AddZipUpload(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def post(self, request):
        """
        上传文件
        :param request:django
        :return:
        """
        try:
            filetype = request.POST.get("type", None)
            id = request.POST.get("id", None)
            # file_path = filetype
            # file_path = 'c:\\DD'.format(filetype)
            file_path = 'c:\\DD'
            if not os.path.exists(file_path):
                os.makedirs(file_path)
            File = request.FILES.get("files", None)
            # print(File.size)

            with open("{0}/{1}".format(file_path, File.name), 'wb+') as f:
                # 分块写入文件
                for chunk in File.chunks():
                    f.write(chunk)

            data={
                "filename": File.name,
                "fileurl": file_path,
                "type": "zip",
                "status": True,
                "fileid": int(id)
            }
            filedata = uploadfile.objects.create(**data)

            # z = zipfile.ZipFile('C:\\DD\\allure-2.7.0.zip', 'r')
            z = zipfile.ZipFile(''.join([file_path, '\\', File.name]), 'r')
            # z.extractall(path=r"C:\\DD")
            z.extractall(path=file_path)
            z.close()

            if os.path.exists(''.join([file_path, '\\', File.name])):  # 如果文件存在
                # 删除文件，可使用以下两种方法。
                os.remove(''.join([file_path, '\\', File.name]))
                # os.unlink(path)


            return JsonResponse(code="0", msg="成功", data={"filename": File.name, "fileid": filedata.id}
                                )
        except Exception as e:
            logger.info(e)
            return JsonResponse(code="999995", msg="上传文件失败！")

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
            file_name = "{0}/{1}".format(obj.fileurl, obj.filename)
            os.remove(file_name)
            return JsonResponse(code="0", msg="删除成功")
        except ObjectDoesNotExist:
            return JsonResponse(code="999995", msg="没有需要上传的文件！")
