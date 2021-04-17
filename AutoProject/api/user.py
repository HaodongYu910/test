from rest_framework import parsers, renderers
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.views import APIView

from AutoProject.serializers import TokenSerializer
from AutoProject.common.api_response import JsonResponse


class ObtainAuthToken(APIView):
    throttle_classes = ()
    permission_classes = ()
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)
    serializer_class = AuthTokenSerializer

    def post(self, request, *args, **kwargs):
        """
        用户登录
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        serializer = self.serializer_class(data=request.data,
                                           context={"request": request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        # token, created = Token.objects.get_or_create(user=user)
        try:
            data = TokenSerializer(Token.objects.get(user=user)).data
            data["roles"]=['admin']
            data["introduction"]= 'administrator'
            data["avatar"]= 'https://wpimg.wallstcn.com/f778738c-e4f8-4870-b634-56703b4acafe.gif',
            # data["name"]= 'Super Admin'
            data["userphoto"] = '/file/img.jpg'
            return JsonResponse(data=data, code="0", msg="成功")
        except Exception as e:
            return JsonResponse(code="900000", msg="登录失败：{}".format(e))


obtain_auth_token = ObtainAuthToken.as_view()

