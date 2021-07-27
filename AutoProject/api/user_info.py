import logging
from rest_framework.authentication import TokenAuthentication

from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.views import APIView

from AutoProject.serializers import TokenSerializer
from AutoProject.common.api_response import JsonResponse

from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction

from rest_framework.parsers import JSONParser

from ..models import Server, User

logger = logging.getLogger(__name__)  # 这里使用 __name__ 动态搜索定义的 logger 配置


class userInfo(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def get(self, request):
        """
        获取用户信息
        :param request:
        :return:
        """
        try:
            token = request.GET.get("token")
        except KeyError:
            return JsonResponse(code="999990", msg="请重新登录用户！")
        try:
            data = TokenSerializer(Token.objects.get(key=token)).data
        except Exception as e:
            return JsonResponse(code="900000", msg="获取信息失败：{}".format(e))

        return JsonResponse(data=data, code="0", msg="成功")


class AddUser(APIView):
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
            Installadd = Token(data=data)

            with transaction.atomic():
                Installadd.is_valid()
                Installadd.save()
            return JsonResponse(code="0", msg="成功")
        except Exception as e:
            return JsonResponse(code="999995", msg="{0}".format(e))


class UpdateUser(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def parameter_check(self, data):
        """
        校验参数
        :param data:
        :return:
        """
        try:
            # 必传参数 token
            if not data["token"]:
                return JsonResponse(code="999996", msg="参数有误 必传参数 token！")

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
            token = Token.objects.get(key=data["token"])
            user = User.objects.get(id=token.user_id)
        except EnvironmentError:
            return JsonResponse(code="999995", msg="数据不存在！")
        try:
            if data["passwd"]:
                if data["password"] == data["passwd"]:
                    user.set_password(data['password'])
                else:
                    return JsonResponse(code="999989", msg="两次密码不一致，请重新输入！")
        except KeyError:
            return JsonResponse(code="999995", msg="密码修改失败！")
        try:
            user.email = data['email']
            user.user.phone = data['phone']
            user.save()
            return JsonResponse(code="0", msg="成功")
        except KeyError:
            return JsonResponse(code="999998", msg="修改失败")


class DelUser(APIView):
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
                    Token.objects.filter(id=j).delete()
                except Exception as e:
                    logger.error("删除Install数据失败")
            return JsonResponse(code="0", msg="成功")
        except ObjectDoesNotExist:
            return JsonResponse(code="999995", msg="项目不存在！")


class DisableUser(APIView):
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
            obj = Token.objects.get(id=data["id"])
            obj.status = False
            obj.save()

            return JsonResponse(code="0", msg="成功")
        except ObjectDoesNotExist:
            return JsonResponse(code="999995", msg="数据不存在！")


class EnableUser(APIView):
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
            pass

            return JsonResponse(code="0", msg="成功")
        except ObjectDoesNotExist:
            return JsonResponse(code="999995", msg="项目不存在！")


