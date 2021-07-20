import logging
from rest_framework.authentication import TokenAuthentication

from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.views import APIView

from AutoProject.serializers import TokenSerializer
from AutoProject.common.api_response import JsonResponse

logger = logging.getLogger(__name__)


class generateRoutes(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

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