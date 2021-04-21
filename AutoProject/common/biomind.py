import threading
from django.conf import settings
from django.db.models import Count, When, Case
from ..models import Server
import os
import subprocess
import time
import logging
from ..utils.keycloak.keycloakadmin import KeycloakAdm
from ..common.transport import SSHConnection

logger = logging.getLogger(__name__)  # 这里使用 __name__ 动态搜索定义的 logger 配置


def Restart(**kwargs):
    id = kwargs["id"]
    server = Server.objects.get(id=id)
    ssh = SSHConnection(host=server.host, pwd=server.pwd)
    try:
        ssh.configure(server.host, str(server.protocol))
        logger.info("Server:{}：重启服务".format(server.host))
        ssh.cmd(
            "sshpass -p {} biomind restart;ls;".format(
                server.pwd))
        time.sleep(300)
        createUser(protocol=server.protocol, server=server.host)
        ssh.close()
    except Exception as e:
        logger.error("Server::{0}：重启服务失败----失败原因：{1}".format(server.host, e))



def createUser( user="biomind3d", pwd="engine3D.", protocol="https", server="192.168.1.208"):
    try:
        user_info = {"username": user,
                     "enabled": True,
                     "credentials": [{
                         "value": pwd,
                         "type": "password",
                     }]}
        kc_adm = KeycloakAdm(orthanc_ip='{0}://{1}'.format(protocol, server))
        # kc_adm.update_user_add_group(user_info, 'admins')
        kc_adm.create_update_user_add_all_group(user_info)
    except Exception as e:
        logging.error('Failed to create User: %s!', e)