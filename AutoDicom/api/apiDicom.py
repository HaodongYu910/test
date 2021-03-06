from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db import transaction
from rest_framework.authentication import TokenAuthentication
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from AutoProject.common.api_response import JsonResponse
from ..models import dicom_group, duration_record, duration, dicom_record
from ..serializers import dicomdata_Deserializer
from ..common.deletepatients import *
from ..common.dicomBase import listUrl, voteData, graphql_query, dicomsavecsv
from ..common.Dicom import SendQueThread
from AutoInterface.models import gold_record
from ..common.anonymous import anonymization
import time
import os

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
            project_id = request.GET.get("project_id", 1)
        except (TypeError, ValueError):
            return JsonResponse(code="999985", msg="page and page_size must be integer!")
        diseases = request.GET.get("diseases")
        slicenumber = request.GET.get("slicenumber")
        dicomtype = request.GET.get("type")
        patientid = request.GET.get("patientid")
        if dicomtype:
            if diseases is not None:
                sql = f"SELECT d.* FROM dicom d JOIN dicom_group_detail gd ON gd.dicom_id = d.id JOIN dicom_group dg ON dg.id = gd.group_id WHERE dg.type ='{dicomtype}' and gd.group_id ='{diseases}' and dg.project_id = {project_id} ORDER BY  d.id "
                obi = dicom.objects.raw(sql)
            else:
                sql = f"SELECT d.* FROM dicom d JOIN dicom_group_detail gd ON gd.dicom_id = d.id JOIN dicom_group dg ON dg.id = gd.group_id WHERE dg.type ='{dicomtype}'  and dg.project_id = {project_id} ORDER BY  d.id "
                obi = dicom.objects.raw(sql)

        elif patientid:
            obi = dicom.objects.filter(patientid__contains=patientid).order_by("-id")
        else:
            if slicenumber != '':
                obi = dicom.objects.filter(slicenumber__contains=slicenumber).order_by("-id")
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


# 修改dicom
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
            if data['patientid'] == obj.patientid and data['patientname'] == obj.patientname:
                pass
            else:
                # 组装匿名数据
                info = {
                    'patientid': data['patientid'],
                    'patientname': data['patientname'],
                    'studyinstanceuid': "",
                }
                # 生成新的路径
                route = obj.route.split("/")
                del route[-1]
                route = '/'.join(route)
                try:
                    file_names = os.listdir(obj.route)
                except ObjectDoesNotExist:
                    return JsonResponse(code="999995", msg="数据不存在！")

                # 判断是否有新增的文件夹
                data['route'] = f"{route}/{data['patientid']}"
                if not os.path.exists(data['route']):
                    os.makedirs(data['route'])
                else:
                    return JsonResponse(code="999993", msg=f"该匿名地址已经存在，请检查：{data['route']}！")
                # 遍历文件匿名相关id name
                for fn in file_names:
                    full_fn = os.path.join(obj.route, fn)
                    full_fake = os.path.join(data['route'], fn)
                    # 调用匿名方法
                    anonymization(
                        full_fn=full_fn,
                        info=info,
                        full_fn_fake=full_fake
                    )
            # 保存修改前信息
            dicom_record.objects.create(**{
                "patientid": obj.patientid,
                "patientname": obj.patientname,
                "studyinstanceuid": obj.studyinstanceuid,
                "dicom_id": obj.id,
                "route": obj.route})
            # 保存修改结果
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
                dicom.objects.filter(id=j).delete()
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
                obj = dicom_group.objects.filter(id__in=data['ids'])
                for i in obj:
                    dicomobj = dicom.objects.filter(fileid=i.id)
                    for j in dicomobj:
                        delete_patients_duration(j.studyinstanceuid, data["server"], "StudyInstanceUID", False)
                    thread_Send = SendQueThread(route=i.content, hostid=host.id)
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
                    obj = gold_record.objects.get(id=data['id'])
                    kc, url = listUrl(obj.gold.Host.id, obj.studyinstanceuid)
                elif type == 'duration':
                    obj = duration_record.objects.get(id=data['id'])
                    kc, url = listUrl(obj.Host_id, obj.studyinstanceuid)
                else:
                    dicomdata = dicom.objects.filter(vote=None)
                if url == False:
                    return JsonResponse(code="999993", msg="未查询到相关数据！")
            except ObjectDoesNotExist:
                return JsonResponse(code="999994", msg="数据错误！")
            return JsonResponse(code="0", msg="成功", data={
                "url": url,
                "kc": kc
            })
        except ObjectDoesNotExist:
            return JsonResponse(code="999995", msg="数据不存在！")


class dicomAnonymization(APIView):
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
        except KeyError:
            return JsonResponse(code="999996", msg="参数有误！")

    def post(self, request):
        """
        修改成功失败
        :param request:
        :return:
        """
        data = JSONParser().parse(request)
        result = self.parameter_check(data)
        if result:
            return result
        try:
            count = 1
            try:
                obj = dicom.objects.filter(id__in=data["ids"])
                for i in obj:
                    if len(data["ids"]) == 1:
                        info = {
                            "studyinstanceuid": '',
                            "patientid": data['PatientID'],
                            "patientname": data['PatientName']

                        }
                    else:
                        info = {
                            "studyinstanceuid": '',
                            "patientid": f"{data['PatientID']}_{count}",
                            "patientname": f"{data['PatientName']}_{count}"

                        }
                    url = i.route.split("/")
                    del url[-1]
                    url = '/'.join(url)
                    file_names = os.listdir(i.route)
                    full_fn_fake = f"{url}/{info['patientid']}"
                    file_names.sort()
                    count = count + 1
                    for fn in file_names:
                        full_fn = os.path.join(i.route, fn)
                        full_fake = os.path.join(full_fn_fake, fn)

                        anonymization(
                            full_fn=full_fn,
                            info=info,
                            full_fn_fake=full_fake
                        )
                    i.patientid = info["patientid"]
                    i.patientname = info["patientname"]
                    i.route = full_fn_fake
                    i.save()

            except ObjectDoesNotExist:
                return JsonResponse(code="999994", msg="数据错误！")
            return JsonResponse(code="0", msg="成功")
        except ObjectDoesNotExist:
            return JsonResponse(code="999995", msg="数据不存在！")
