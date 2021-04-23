import logging

from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db import transaction
from rest_framework.authentication import TokenAuthentication
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView

from AutoProject.common.api_response import JsonResponse
from AutoProject.common.common import record_dynamic
from AutoProject.models import dictionary
from AutoProject.serializers import dictionary_Deserializer, dictionary_Serializer

logger = logging.getLogger(__name__)  # 这里使用 __name__ 动态搜索定义的 logger 配置，这里有一个层次关系的知识点。


class Dictionary(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def get(self, request):
        """
        获取dictionary列表
        :param request:
        :return:
        """
        try:
            page_size = int(request.GET.get("page_size", 20))
            page = int(request.GET.get("page", 1))
            key = request.GET.get("name")
            Dictionarytype = request.GET.get("type")
        except (TypeError, ValueError):
            return JsonResponse(code="999995", msg="page and page_size must be integer！")

        if key:
            obi = dictionary.objects.filter(key__contains=key).order_by("id")
        elif Dictionarytype:
            obi = dictionary.objects.filter(type__contains=Dictionarytype).order_by("id")
        else:
            obi = dictionary.objects.all().order_by("id")

        paginator = Paginator(obi, page_size)  # paginator对象
        total = paginator.num_pages  # 总页数
        try:
            obm = paginator.page(page)
        except PageNotAnInteger:
            obm = paginator.page(1)
        except EmptyPage:
            obm = paginator.page(paginator.num_pages)
        serialize = dictionary_Serializer(obm, many=True)
        return JsonResponse(data={"data": serialize.data,
                                  "page": page,
                                  "total": total
                                  }, code="0", msg="成功！")


class AddDictionary(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def parameter_check(self, data):
        """
        校验参数
        :param data:
        :return:
        """
        try:
            # 必传参数 name, host
            if not data["key"] or not data["value"]or not data["type"]:
                return JsonResponse(code="999995", msg="参数有误！")
        except KeyError:
            return JsonResponse(code="999995", msg="参数有误！")

    def post(self, request):
        """
        添加
        :param request:
        :return:
        """
        data = JSONParser().parse(request)
        result = self.parameter_check(data)
        if result:
            return result
        obi = dictionary.objects.filter(key=data["key"])
        if obi:
            return JsonResponse(code="999997", msg="存在相同key！")
        else:
            serializer = dictionary_Serializer(data=data)
            with transaction.atomic():
                if serializer.is_valid():
                    serializer.save()
                    return JsonResponse(data={
                        "id": serializer.data.get("id")
                    }, code="0", msg="成功！")
                return JsonResponse(code="999998", msg="失败！")


class UpdateDictionary(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def parameter_check(self, data):
        """
        校验参数
        :param data:
        :return:
        """
        try:
            # 校验dictionary_id类型为int
            if not isinstance(data["id"], int):
                return JsonResponse(code="999995", msg="参数有误！")
            # 必传参数 name, host
            if not data["key"] or not data["value"]:
                return JsonResponse(code="999995", msg="参数有误！")
        except KeyError:
            return JsonResponse(code="999995", msg="参数有误！")

    def post(self, request):
        """
        修改
        :param request:
        :return:
        """
        data = JSONParser().parse(request)
        result = self.parameter_check(data)
        if result:
            return result
        try:
            obi = dictionary.objects.get(id=data["id"])
        except ObjectDoesNotExist:
            return JsonResponse(code="999992", msg="不存在！")
        key = dictionary.objects.filter(key=data["key"]).exclude(id=data["id"])
        if len(key):
            return JsonResponse(code="999997", msg="存在相同key！")
        else:
            serializer = dictionary_Serializer(data=data)
            with transaction.atomic():
                if serializer.is_valid():
                    # 外键dictionary_id
                    serializer.update(instance=obi, validated_data=data)
                    return JsonResponse(code="0", msg="成功！")
                return JsonResponse(code="999998", msg="失败！")


class DelDictionary(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def parameter_check(self, data):
        """
        校验参数
        :param data:
        :return:
        """
        try:
            # 校验dictionary_id类型为int
            if not isinstance(data["ids"], list):
                for i in data["ids"]:
                    if not isinstance(i, int):
                        return JsonResponse(code="999995", msg="参数有误！")
                return JsonResponse(code="999995", msg="参数有误！")
        except KeyError:
            return JsonResponse(code="999995", msg="参数有误！")

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
                dictionary.objects.filter(id=j).delete()
            return JsonResponse(code="0", msg="成功！")
        except ObjectDoesNotExist:
            return JsonResponse(code="999995", msg="项目不存在！")


class DisableDictionary(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def parameter_check(self, data):
        """
        校验参数
        :param data:
        :return:
        """
        try:
            # 校验dictionary_id类型为int
            if not isinstance(data["id"], int):
                return JsonResponse(code="999995", msg="参数有误！")
        except KeyError:
            return JsonResponse(code="999995", msg="参数有误！")

    def post(self, request):
        """
        禁用
        :param request:
        :return:
        """
        data = JSONParser().parse(request)
        result = self.parameter_check(data)
        if result:
            return result
        try:
            obj = dictionary.objects.get(id=data["id"])
        except ObjectDoesNotExist:
            return JsonResponse(code="999992", msg="不存在")
        obj.status = False
        obj.save()
        return JsonResponse(code="0", msg="成功！")


class EnableDictionary(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def parameter_check(self, data):
        """
        校验参数
        :param data:
        :return:
        """
        try:
            # 校验dictionary_id类型为int
            if not isinstance(data["id"], int):
                return JsonResponse(code="999995", msg="参数有误！")
        except KeyError:
            return JsonResponse(code="999995", msg="参数有误！")

    def post(self, request):
        """
        启用
        :param request:
        :return:
        """
        data = JSONParser().parse(request)
        result = self.parameter_check(data)
        if result:
            return result
        try:
            obj = dictionary.objects.get(id=data["id"])
        except ObjectDoesNotExist:
            return JsonResponse(code="999992", msg="不存在")
        obj.status = True
        obj.save()

        return JsonResponse(code="0", msg="成功！")
