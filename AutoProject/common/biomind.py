import threading
from django.conf import settings
from django.db.models import Count, When, Case
from ..models import Server
import os
import subprocess
import time
from ..utils.keycloak.keycloakadmin import KeycloakAdm
from ..common.transport import SSHConnection

from AutoInterface.models import gold_test
from AutoInterface.common.gold import GoldThread

from AutoDicom.models import duration
from AutoDicom.common.duration import durationSend
from AutoProject.models import project_version, Server
import logging

logger = logging.getLogger(__name__)  # 这里使用 __name__ 动态搜索定义的 logger 配置


# 服务器重启
def Restart(**kwargs):
    try:
        server = Server.objects.get(id=kwargs["id"])
        ssh = SSHConnection(host=server.host, pwd=server.pwd)
        ssh.configure(server.host, str(server.protocol))
        logger.info("Server:{}：重启服务".format(server.host))
        ssh.command(f"nohup sshpass -p {server.pwd} biomind restart > restart.log 2>&1 &")
        time.sleep(300)
        createUser(protocol=server.protocol, server=server.host)

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
                    "/home/biomind/orthanc.json")
        ssh.upload("/files1/classifier/cache.zip",
                    "/home/biomind/cache.zip")
        ssh.cmd(
            "unzip -o cache.zip -d /home/biomind/.biomind/var/biomind/;")
        ssh.cmd(
            "mv -f orthanc.json /home/biomind/.biomind/var/biomind/orthanc/orthanc.json")
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
            "dicom": "78",
            "sendcount": 258,
            "sleepcount": 100,
            "sleeptime": 3,
            "series": False,
            "sendstatus": True,
            "status": True,
            "Host_id": 13,
            "type": 3,
            "version": kwargs["version"]
        }
        logger.info("创建持续化测试:{}".format(data))
        obj = duration.objects.create(**data)

        logger.info("Nightly Build Version:{}：执行持续化测试".format(kwargs["version"]))
        durationSend(obj.id)
    except Exception as e:
        logger.error("Version:{0}：执行持续化测试报错{1}".format(kwargs["version"], e))


def smoke(version):
    try:
        obj = project_version.objects.get(version=version, type='3')
        versionID = obj.id
    except:
        try:
            versionOBJ = project_version.objects.create(**{
                "version": version,
                "branch": "master",
                "package_name": None,
                "path": None,
                "type": "3",
                "project_id": 1,
                "status": True,
            })
            versionID = versionOBJ.id
        except Exception as e:
            logger.error(e)

    try:
        logger.info("Nightly Build Version:{}：更新配置文件".format(version))
        cache(id=13)
        logger.info("Nightly Build Version:{}：重启服务".format(version))
        Restart(id=13)
        time.sleep(300)
        createUser(server="192.168.2.103")
        logger.info("Nightly Build Version:{}：金标准测试".format(version))
        goldsmoke(version=versionID)
        HostObj = Server.objects.get(id=13)
        logger.info("Nightly Build Version:{}：持续化测试".format(version))
        durationTest(version=versionID, server=HostObj.host, aet=HostObj.remarks)
    except Exception as e:
        logger.error("Nightly Build Version：执行{0}版本冒烟失败----失败原因：{1}".format(version, e))
