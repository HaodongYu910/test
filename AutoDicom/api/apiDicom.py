from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db import transaction
from rest_framework.authentication import TokenAuthentication
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from AutoTest.common.api_response import JsonResponse
from ..models import dicom_base, duration_record
from ..serializers import dicomdata_Deserializer
from ..common.deletepatients import *
from ..common.dicomBase import listUrl, voteData, graphql_query, dicomsavecsv
from ..common.Dicom import SendQueThread

logger = logging.getLogger(__name__)  # 这里使用 __name__ 动态搜索定义的 logger 配置


class dicomDetail(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def parameter_check(self, data):
        """
        校验参数
        :param data:
        :return:
        """
        try:
            # 必传参数 server
            if not data["server"]:
                return JsonResponse(code="999996", msg="参数有误,必传参数 server！")

        except KeyError:
            return JsonResponse(code="999996", msg="参数有误！")

    def post(self, request):
        """
        send数据
        :param request:
        :return:
        """
        data = JSONParser().parse(request)
        result = self.parameter_check(data)
        if result:
            return result
        try:
            kc = login_keycloak(data['server'])
            obj = Server.objects.get(id=data['server'])
            try:
                if data['ids']:
                    dicomdata = dicom.objects.filter(id__in=data['ids'])
                elif data['diseases']:
                    dicomdata = dicom.objects.filter(diseases=data['diseases'])
                else:
                    dicomdata = dicom.objects.filter(vote=None)

                for i in dicomdata:
                    try:
                        objdictionary = dictionary.objects.get(id=i.predictor)
                        if i.vote is None:
                            i.vote, i.imagecount, i.slicenumber = voteData(i.studyinstanceuid, obj.host,
                                                                           i.predictor, kc)
                        vote = i.vote
                        i.graphql = graphql_query(i.studyinstanceuid, vote, i.predictor, objdictionary.value)
                        i.save()
                    except Exception as e:
                        logger.error(e)
                        continue

            except ObjectDoesNotExist:
                return JsonResponse(code="999994", msg="数据未预测，请先预测！")
            return JsonResponse(code="0", msg="成功")
        except ObjectDoesNotExist:
            return JsonResponse(code="999995", msg="数据不存在！")


class dicomData(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def get(self, request):
        """
        获取dicom数据列表
        :param request:
        :return:
        """
        try:
            page_size = int(request.GET.get("page_size", 20))
            page = int(request.GET.get("page", 1))
        except (TypeError, ValueError):
            return JsonResponse(code="999985", msg="page and page_size must be integer!")
        diseases = request.GET.get("diseases")
        slicenumber = request.GET.get("slicenumber")
        dicomtype = request.GET.get("type")
        if dicomtype:
            if diseases == '' and slicenumber != '':
                obi = dicom.objects.filter(slicenumber__contains=slicenumber, type=dicomtype).order_by("-id")
            elif diseases != '' and slicenumber == '':
                obi = dicom.objects.filter(diseases__contains=diseases, type=dicomtype).order_by("-id")
            elif diseases != '' and slicenumber != '':
                obi = dicom.objects.filter(diseases__contains=diseases, slicenumber__contains=slicenumber,
                                           type=dicomtype).order_by("-id")
            else:
                obi = dicom.objects.filter(type=dicomtype).order_by("-id")
        else:
            if diseases == '' and slicenumber != '':
                obi = dicom.objects.filter(slicenumber__contains=slicenumber).order_by("-id")
            elif diseases != '' and slicenumber == '':
                obi = dicom.objects.filter(diseases__contains=diseases).order_by("-id")
            elif diseases != '' and slicenumber != '':
                obi = dicom.objects.filter(diseases__contains=diseases, slicenumber__contains=slicenumber).order_by(
                    "-id")
            else:
                obi = dicom.objects.all().order_by("-id")

        paginator = Paginator(obi, page_size)  # paginator对象
        total = paginator.num_pages  # 总页数
        try:
            obm = paginator.page(page)
        except PageNotAnInteger:
            obm = paginator.page(1)
        except EmptyPage:
            obm = paginator.page(paginator.num_pages)
        serialize = dicomdata_Deserializer(obm, many=True)
        return JsonResponse(data={"data": serialize.data,
                                  "page": page,
                                  "total": total
                                  }, code="0", msg="成功")



# 修改duration
class dicomUpdate(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def parameter_check(self, data):
        """
        校验参数
        :param data:
        :return:
        """
        try:
            # 必传参数 key, server_ip , type
            if not data["id"]:
                return JsonResponse(code="999996", msg="参数有误,必传参数 id！")

        except KeyError:
            return JsonResponse(code="999996", msg="参数有误！")

    def post(self, request):
        """
        send数据
        :param request:
        :return:
        """
        data = JSONParser().parse(request)
        result = self.parameter_check(data)
        if result:
            return result
        try:
            obj = dicom.objects.get(id=data["id"])
            serializer = dicomdata_Deserializer(data=data)
            with transaction.atomic():
                if serializer.is_valid():
                    # 修改数据
                    serializer.update(instance=obj, validated_data=data)
                return JsonResponse(code="0", msg="成功")
        except ObjectDoesNotExist:
            return JsonResponse(code="999995", msg="数据不存在！")


# 删除dicom 数据
class deldicomdata(APIView):
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
        删除
        :param request:
        :return:
        """
        data = JSONParser().parse(request)
        result = self.parameter_check(data)
        if result:
            return result
        try:
            for j in data["ids"]:
                obj = dicom.objects.filter(id=j)
                obj.delete()
            return JsonResponse(code="0", msg="成功")
        except ObjectDoesNotExist:
            return JsonResponse(code="999995", msg="数据不存在！")


class DisableDicom(APIView):
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
        禁用数据
        :param request:
        :return:
        """
        data = JSONParser().parse(request)
        result = self.parameter_check(data)
        if result:
            return result
        # 查找是否存在
        try:
            obj = dicom.objects.get(id=data["id"])
            obj.status = False
            obj.save()
            return JsonResponse(code="0", msg="成功")
        except ObjectDoesNotExist:
            return JsonResponse(code="999995", msg="项目不存在！")


class EnableDicom(APIView):
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
        启用数据
        :param request:
        :return:
        """
        data = JSONParser().parse(request)
        result = self.parameter_check(data)
        if result:
            return result
        try:
            obj = dicom.objects.get(id=data["id"])
            obj.status = True
            # 变更状态
            obj.save()

            return JsonResponse(code="0", msg="成功")
        except ObjectDoesNotExist:
            return JsonResponse(code="999995", msg="项目不存在！")


class dicomSend(APIView):
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
            # 必传参数  server_ip
            if not data["server"]:
                return JsonResponse(code="999996", msg="参数有误,必传参数 server_ip！")

        except KeyError:
            return JsonResponse(code="999996", msg="参数有误！")

    def post(self, request):
        """
        删除
        :param request:
        :return:
        """
        data = JSONParser().parse(request)
        result = self.parameter_check(data)
        if result:
            return result
        try:
            host = Server.objects.get(id=data["server"])
            if data['ids']:
                obj = dicom_base.objects.filter(id__in=data['ids'])
                for i in obj:
                    dicomobj = dicom.objects.filter(fileid=i.id)
                    for j in dicomobj:
                        delete_patients_duration(j.studyinstanceuid, data["server"], "StudyInstanceUID", False)
                    thread_Send = SendQueThread(route=i.content,hostid=host.id)
                    thread_Send.start()
            else:
                obj = dicom.objects.filter(id__in=data['id'])
                for i in obj:
                    thread_Send = SendQueThread(route=i.route, hostid=host.id)
                    thread_Send.start()

            return JsonResponse(code="0", msg="成功")
        except ObjectDoesNotExist:
            return JsonResponse(code="999995", msg="数据不存在！")


class dicomcsv(APIView):
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
        删除
        :param request:
        :return:
        """
        data = JSONParser().parse(request)
        result = self.parameter_check(data)
        if result:
            return result
        try:
            dicomsavecsv(data["ids"])
            return JsonResponse(code="0", msg="成功")
        except ObjectDoesNotExist:
            return JsonResponse(code="999995", msg="数据不存在！")


class dicomUrl(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def parameter_check(self, data):
        """
        校验参数
        :param data:
        :return:
        """
        try:
            # 必传参数 type
            if not data["type"]:
                return JsonResponse(code="999996", msg="参数有误,必传参数 type, id！")

        except KeyError:
            return JsonResponse(code="999996", msg="参数有误！")

    def post(self, request):
        """
        返回url
        :param request:
        :return:
        """
        data = JSONParser().parse(request)
        result = self.parameter_check(data)
        if result:
            return result
        try:
            type = data['type']
            try:
                if type == 'gold':
                    obj = dicom.objects.get(id=data['id'])
                    kc, url = listUrl(obj.hostid, obj.studyinstanceuid)
                elif type == 'duration':
                    obj = duration_record.objects.get(id=data['id'])
                    kc, url = listUrl(obj.hostid, obj.studyinstanceuid)
                else:
                    dicomdata = dicom.objects.filter(vote=None)
            except ObjectDoesNotExist:
                return JsonResponse(code="999994", msg="数据未预测，请先预测！")
            return JsonResponse(code="0", msg="成功", data={
                "url": url,
                "kc": kc
            })
        except ObjectDoesNotExist:
            return JsonResponse(code="999995", msg="数据不存在！")
