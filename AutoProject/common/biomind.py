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

from AutoInterface.models import gold_test
from AutoInterface.common.gold import GoldThread

from AutoDicom.models import duration
from AutoDicom.common.durarion import DurationThread

logger = logging.getLogger(__name__)  # 这里使用 __name__ 动态搜索定义的 logger 配置


# biomind命令

# 服务器重启
def Restart(**kwargs):
    try:
        server = Server.objects.get(id=kwargs["id"])
        ssh = SSHConnection(host=server.host, pwd=server.pwd)
        ssh.configure(server.host, str(server.protocol))
        logger.info("Server:{}：重启服务".format(server.host))
        ssh.command("nohup sshpass -p {} biomind restart > restart.log 2>&1 &".format(server.pwd))
        time.sleep(300)
        createUser(protocol=server.protocol, server=server.host)
        ssh.close()
    except Exception as e:
        logger.error("Server::{0}：重启服务失败----失败原因：{1}".format(server.host, e))

# keyclack 创建用户
def createUser(user="biomind3d", pwd="engine3D.", protocol="https", server="192.168.1.208"):
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

# 更新 cache文件
def cache(**kwargs):
    try:
        server = Server.objects.get(id=kwargs["id"])
        ssh = SSHConnection(host=server.host, pwd=server.pwd)
        ssh.cmd("rm -rf cache.zip;")
        ssh.upload("/files1/classifier/orthanc.json",
                   "/home/biomind/.biomind/var/biomind/orthanc/orthanc.json")
        ssh.upload("/files1/classifier/cache.zip",
                   "/home/biomind/cache.zip")
        ssh.cmd(
            "mv /home/biomind/.biomind/var/biomind/cache cachebak;unzip -o cache.zip -d /home/biomind/.biomind/var/biomind/;")
        ssh.close()
    except Exception as e:
        logger.error("更新配置文件失败----失败原因：{0}".format(e))

# 创建冒烟测试 且执行
def goldsmoke(version):
    try:
        logger.info("{}版本：创建金标准测试".format(version))
        data = {"version": version,
                "diseases": "19,44,31,32,21,33,23,24,20,30,22,25,26",
                "status": True,
                "Host_id": 13,
                "thread": 1,
                "count": 127
                }

        Obj = gold_test.objects.create(**data)

        logger.info("{}版本：执行金标准测试".format(version))
        testThread = GoldThread(Obj.id, "goldNightly")
        # 设为保护线程，主进程结束会关闭线程
        testThread.setDaemon(True)
        # 开始线程
        testThread.start()
    except Exception as e:
        logger.error("Version:{0}：执行金标准测试报错{1}".format(version, e))

# 创建 持续化测试且执行
def durationTest(**kwargs):
    try:
        data = {
                "server": kwargs["server"],
                "port": 4242,
                "aet": kwargs["aet"],
                "patientid": 'DT',
                "patientname": 'Dt',
                "dicom": "1,2,3,4,5,6,7,8,9,10,11,13,14,35,45",
                "sendcount": 258,
                "sleepcount": 100,
                "sleeptime": 3,
                "series": False,
                "sendstatus": True,
                "status": True,
                "Host_id": 13,
                "type": "Nightly",
                "version": kwargs["version"]
                }
        logger.info("创建持续化测试:{}".format(data))
        obj = duration.objects.create(**data)

        logger.info("Nightly Build Version:{}：执行持续化测试".format(kwargs["version"]))
        testThread = DurationThread(id=obj.id)
        # 设为保护线程，主进程结束会关闭线程
        testThread.setDaemon(True)
        # 开始线程
        testThread.start()
    except Exception as e:
        logger.error("Version:{0}：执行持续化测试报错{1}".format(kwargs["version"], e))

# 创建UI测试且执行
# def UiTest(**kwargs):
#     try:
#         data = {"version": self.obj.version,
#                 "setup": "1",
#                 "cases": "1",
#                     "tearDown": "1",
#                     "status": True,
#                     "hostid": self.obj.hostid,
#                     "thread": 1
#                     }
#             logger.info("Nightly Build Version:{}：创建UI测试".format(self.version))
#             uobj = autoui.objects.create(**data)
#             self.obj.type = 6
#             self.obj.uid = uobj.id
#             self.obj.save()
#             # testThread = GoldThread(smokeobj.id)
#             # # 设为保护线程，主进程结束会关闭线程
#             # testThread.setDaemon(True)
#             # # 开始线程
#             # testThread.start()
#         except Exception as e:
#             logger.error("Nightly Build Version:{0}：执行UI自动化报错{1}".format(self.version, e))
