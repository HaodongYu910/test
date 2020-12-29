
import logging
from .keycloakclient import KeycloakClient
from ...models import GlobalHost
logger = logging.getLogger(__name__)  # 这里使用 __name__ 动态搜索定义的 logger 配置，这里有一个层次关系的知识点。


def login_keycloak(id):
    '''
    Log in to keycloak to obtain authentication authority 登录keycloak，获取认证权限
    :returns: KeycloakClient(type: object) message: success/ failed
    '''

    # keycloak 用户名
    username = 'biomind3d'
    password = 'engine3D.'
    obj = GlobalHost.objects.get(id=id)
    try:
        kc = KeycloakClient('{0}://{1}'.format(
            obj.protocol,obj.host), username,
            password)
        kc.login(username,password)
    except Exception as e:
        msg_code = 'kc_001'
        logger.info("Keycloak 登录失败:{0}".format(e))
        return msg_code
    return kc
