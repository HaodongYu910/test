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
            type = request.GET.get("type")
        except (TypeError, ValueError):
            return JsonResponse(code="999985", msg="page and page_size must be integer!")
        filename = request.GET.get("filename")

        if filename:
            obi = uploadfile.objects.filter(filename=filename, type=type).order_by("id")
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

            with open("{0}/{1}".format(file_path, File.name), 'wb+') as f:
                # 分块写入文件
                for chunk in File.chunks():
                    f.write(chunk)

            fileData = uploadfile.objects.create(**{
                "filename": File.name,
                "fileurl": file_path,
                "type": filetype,
                "status": True
            })
            return JsonResponse(code="0", msg="成功", data={
                "filename": File.name,
                "fileid": fileData.id
            }
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

def gengming(file_path):
    filelist = os.listdir(file_path)
    for old_name in filelist:
        path = os.path.join(file_path, old_name)
        # print(path)
        a = os.path.isdir(path)
        if a:  # 如果它是个文件夹
            new_name = ""
            try:

                # try:
                new_name = old_name.encode('cp437').decode('gbk')
                # except Exception as e:
                #     new_name = old_name.encode('utf-8').decode('utf-8')

                old_name = os.path.join(file_path, old_name)
                new_name = os.path.join(file_path, new_name)
                os.rename(old_name, new_name)
                gengming(new_name)
                continue
            except Exception as e:
                print(e)
            if new_name == "":
                gengming(path)
                continue
            break


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
            fileId = request.POST.get("id")
            custom = request.POST.get("custom")
            if custom is None:
                return JsonResponse(code="999995", msg="路径不能为空！")
            remark = str(custom).split('/')[-1]
            data = {
                # "filename": filename,
                "fileurl": custom,
                # "type": "zip",
                # "size": File.size,
                "status": True,
                "fileid": int(fileId),
                "remark": remark
            }
            filedata = uploadfile.objects.create(**data)

            # 创建线程
            thread_fake_folder = threading.Thread(target=fileUpdate,
                                                  args=(fileId,))
            # 启动线程
            thread_fake_folder.start()

            return JsonResponse(code="0", msg="成功", data={"fileid": filedata.id, "file_path": custom}
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
