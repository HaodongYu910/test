
import logging
from .keycloakclient import KeycloakClient
from ...models import Server
from .keycloakadmin import KeycloakAdm
logger = logging.getLogger(__name__)  # 这里使用 __name__ 动态搜索定义的 logger 配置，这里有一个层次关系的知识点。


def login_keycloak(id):
    '''
    Log in to keycloak to obtain authentication authority 登录keycloak，获取认证权限
    :returns: KeycloakClient(type: object) message: success/ failed
    '''

    # keycloak 用户名
    username = 'biomind3d'
    password = 'engine3D.'
    obj = Server.objects.get(id=id)
    try:
        kc = KeycloakClient('{0}://{1}'.format(
            obj.protocol, obj.host), username,
            password)
        kc.login(username, password)
    except Exception as e:
        logger.info("Keycloak 登录失败:{0}".format(e))
        user_info = {"username": "biomind3d", "enabled": True,
                     "credentials": [{"value": "engine3D.", "type": "password", }]}
        kc_adm = KeycloakAdm(orthanc_ip='{0}://{1}'.format(obj.protocol, obj.host))
        # kc_adm.update_user_add_group(user_info, 'admins')
        kc_adm.create_update_user_add_all_group(user_info)
        kc = KeycloakClient('{0}://{1}'.format(
            obj.protocol, obj.host), username,
            password)
        kc.login(username, password)
        return kc
    return kc
