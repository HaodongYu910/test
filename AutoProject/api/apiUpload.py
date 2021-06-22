import threading
import time

from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from rest_framework.authentication import TokenAuthentication
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView

from AutoDicom.common.dicomfile import fileUpdate
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


def makedir(file_path, filename):
    # 按当前时间创建文件夹，为本次补充病人数据的跟目录
    path = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    path = path.replace(":", "-")
    path = str(file_path) + "/" + str(filename) + "----" + str(path)
    # 去除首位空格
    path = path.strip()
    # 去除尾部 \ 符号
    path = path.rstrip("/")
    # 判断路径是否存在
    isExists = os.path.exists(path)
    # 判断结果
    if not isExists:
        # 如果不存在则创建目录
        # 创建目录操作函数
        os.makedirs(path)
        return path
    else:
        # 如果目录存在则不创建，并提示目录已存在
        logger.info("文件夹已存在")
        raise Exception("文件夹已存在")


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
            # start = time.clock()
            filetype = request.POST.get("type", None)
            # end = time.clock()
            # print('Running time: %s Seconds'%(end-start))
            fileId = request.POST.get("id")
            File = request.FILES.get("files", None)
            custom = request.POST.get("custom")

            filename = File.name

            if custom is None:
                custom = filename[:filename.index("-")]
            # 建立文件夹用来存放病人数据，每上传一次就建立一个，名称是自定义名称加时间
            # file_path = 'e:\\DD'
            file_path = filetype
            file_path = makedir(file_path, custom)

            FilePath = "{0}/{1}".format(file_path, filename)
            with open(FilePath, 'wb+') as f:
                # 分块写入文件
                for chunk in File.chunks():
                    f.write(chunk)
                    # 试试获取文件大小
                    # actualSize = os.path.getsize(FilePath)
                    # print(actualSize)

            # 解压压缩包
            if "zip" in str(filename):
                z = zipfile.ZipFile(''.join([file_path, '/', filename]), 'r')
                z.extractall(path=file_path)
                z.close()
            elif "rar" in str(filename):
                os.system(f"unrar x {file_path}/{filename}")
            elif "tar" in str(filename):
                os.system(f"tar -xzvf {file_path}/{filename}")
            else:
                return JsonResponse(code="999995", msg="解压文件失败 类型不正确！")

            # 删除压缩包
            if os.path.exists(''.join([file_path, '/', filename])):
                os.remove(''.join([file_path, '/', filename]))

            data = {
                "filename": filename,
                "fileurl": file_path,
                "type": "zip",
                "size": File.size,
                "status": True,
                "fileid": int(fileId),
                "remark": custom
            }
            filedata = uploadfile.objects.create(**data)

            # 创建线程
            thread_fake_folder = threading.Thread(target=fileUpdate,
                                                  args=(fileId,))
            # 启动线程
            thread_fake_folder.start()

            return JsonResponse(code="0", msg="成功", data={"filename": File.name, "fileid": filedata.id, "file_path":file_path}
                                )
        except Exception as e:
            logger.error(e)
            return JsonResponse(code="999995", msg="上传文件失败！")


class getProgress(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def post(self, request):
        """
        上传文件
        :param request:django
        :return:
        """
        try:
            id = request.data.get("id", None)
            print(id)
            fileList = uploadfile.objects.filter(fileid=id).order_by('id')
            files = list(fileList)
            if len(files) > 0:
                file = files[-1]
                size = int(file.size)
                if size is not None:
                    actualSize = int(os.path.getsize(file.fileurl,file.filename))
                    print('yinggai=', size)
                    print('实际=', actualSize)
                else:
                    return JsonResponse(code="999995", msg="该病种没有上传任何数据!")
            else:
                return JsonResponse(code="999995", msg="未找到该病种！")

            return JsonResponse(code="0", msg="成功", data={"bfb": 10}
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
