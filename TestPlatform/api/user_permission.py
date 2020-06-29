import logging
from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView

from TestPlatform.common.api_response import JsonResponse
# from TestPlatform.common.common import record_dynamic
# from TestPlatform.models import stressrecord
# from TestPlatform.serializers import stressrecord_Serializer, stressrecord_Deserializer
# from TestPlatform.common.regexUtil import *
# from TestPlatform.common.Loadtest import *

logger = logging.getLogger(__name__)

class userinfo(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()
    def get(self, request):
        """
        获取用户权限
        :param request:
        :return:
        """

        info = {
            'roles': ['admin'],
            'introduction': 'administrator',
            'avatar': 'https://wpimg.wallstcn.com/f778738c-e4f8-4870-b634-56703b4acafe.gif',
            'name': 'Super Admin'}

        return JsonResponse(data=info, code="0", msg="成功")


class generateRoutes(APIView):
    def get(self, request):
        """
        获取用户权限
        :param request:
        :return:
        """
        routes = {}
        roles = [{
                'key': 'admin',
                'name': 'admin',
                'description': 'Administrator',
                'routes': routes
            },
            {
                'key': 'editor',
                'name': 'editor',
                'description': 'Normal Editor',
                'routes': 'routes.filter(i= > i.path != = "/permission")'
        },
        {
            'key': 'visitor',
            'name': 'visitor',
            'description': 'Just a visitor. Can only see the home page and the document page',
            'routes': [{
                'path': '',
                'redirect': 'dashboard',
                'children': [
                    {
                        'path': 'dashboard',
                        'name': 'Dashboard',
                        'meta': {'title': 'dashboard', 'icon': 'dashboard'}
                    }
                ]
            }]
        }
        ]
        info = {
            'roles': ['admin'],
            'introduction': 'administrator',
            'avatar': 'https://wpimg.wallstcn.com/f778738c-e4f8-4870-b634-56703b4acafe.gif',
            'name': 'Super Admin'}

        return JsonResponse(data=info, code="0", msg="成功")
