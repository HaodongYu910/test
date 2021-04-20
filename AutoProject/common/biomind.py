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


class CacheThread(threading.Thread):
    def __init__(self, **kwargs):
        threading.Thread.__init__(self)
        self.Flag = True  # 停止标志位
        # self.count = kwargs["count"]  # 可用来被外部访问的
        # 性能测试id
        self.id = kwargs["id"]
        self.server = Server.objects.get(id=self.id)
        self.ssh = SSHConnection(host=self.server.host, pwd=self.server.pwd)

    def run(self):
        try:
            logger.info("Nightly Build Version:{}：更新 orthanc 文件".format(self.version))
            self.ssh.upload("/files1/classifier/orthanc.json",
                                "/home/biomind/.biomind/var/biomind/orthanc/orthanc.json")
            self.ssh.upload("/files1/classifier/cache.zip",
                                "/home/biomind/cache.zip")
            logger.info("Nightly Build Version:{}：解压cache文件".format(self.id))
            self.ssh.cmd(
                    "unzip -o cache.zip -d /home/biomind/.biomind/var/biomind/;")

        except Exception as e:
            logger.error("Nightly Build Version:{0}：更新json文件失败----失败原因：{1}".format(self.version, e))



            logger.info("Nightly Build Version:{}：sheep 300 秒".format(self.version))
            time.sleep(300)
            self.createUser()
            logger.info("Nightly Build Version:{}：createUser".format(self.version))
            self.goldsmoke()
            self.duration()
        except Exception as e:
            logger.error("Nightly Build Version:{0}：安装{1}版本失败----失败原因：{2}".format(self.version, self.obj.version, e))

    def setFlag(self, parm):  # 外部停止线程的操作函数
        handle = os.getpid()
        subprocess.Popen("taskkill /F /T /PID " + str(handle), shell=True)
        self.Flag = parm  # boolean

    def setParm(self, parm):  # 外部修改内部信息函数
        self.Parm = parm

    def getParm(self):  # 外部获得内部信息函数
        return self.parm

class RestartThread(threading.Thread):
    def __init__(self, **kwargs):
        threading.Thread.__init__(self)
        self.Flag = True  # 停止标志位
        # self.count = kwargs["count"]  # 可用来被外部访问的
        # 性能测试id
        self.id = kwargs["id"]
        self.server = Server.objects.get(id=self.id)
        self.ssh = SSHConnection(host=self.server.host, pwd=self.server.pwd)

    def run(self):
        try:
            self.ssh.configure(self.server.host, str(self.server.protocol))
            logger.info("Server:{}：重启服务".format(self.server.host))
            self.ssh.cmd(
                        "sshpass -p {} biomind restart;ls;".format(
                            self.server.pwd))
            time.sleep(300)
            self.createUser()
            self.ssh.close()
        except Exception as e:
            logger.error("Server::{0}：重启服务失败----失败原因：{1}".format(self.server.host, e))


    def createUser(self):
        try:
            logger.info("Nightly Build Version:{}：创建 3d 用户".format(self.version))
            user_info = {"username": "biomind3d", "enabled": True,
                         "credentials": [{"value": "engine3D.", "type": "password", }]}
            kc_adm = KeycloakAdm(orthanc_ip='{0}://{1}'.format(self.server.protocol, self.server.host))
            # kc_adm.update_user_add_group(user_info, 'admins')
            kc_adm.create_update_user_add_all_group(user_info)
        except Exception as e:
            logging.error('Failed to create User: %s!', e)

    def setFlag(self, parm):  # 外部停止线程的操作函数
        handle = os.getpid()
        subprocess.Popen("taskkill /F /T /PID " + str(handle), shell=True)
        self.Flag = parm  # boolean

    def setParm(self, parm):  # 外部修改内部信息函数
        self.Parm = parm

    def getParm(self):  # 外部获得内部信息函数
        return self.parm
