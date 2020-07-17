import traceback
import logging
from .keycloakclient import KeycloakClient



def login_keycloak(orthanc_ip,orthanc_port,viewer_username,viewer_password):
    '''
    Log in to keycloak to obtain authentication authority 登录keycloak，获取认证权限
    :returns: KeycloakClient(type: object) message: success/ failed
    '''
    try:
        kc = KeycloakClient('https://{0}:{1}'.format(
            orthanc_ip, orthanc_port), viewer_username,
            viewer_password)
        kc.login(viewer_username,viewer_password)
    except Exception as e:
        msg_code = 'kc_001'
        return None, msg_code
    return kc, None
