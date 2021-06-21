
from AutoProject.models import project_version, Server
import logging, time
from AutoProject.common.biomind import createUser, cache, Restart, goldsmoke, durationTest

import datetime
import time
import threading

logger = logging.getLogger(__name__)


# 执行冒烟测试
class SMThread(threading.Thread):
    def __init__(self, version):
        threading.Thread.__init__(self)
        self.version = version

    def run(self):
        try:
            obj = project_version.objects.get(version=self.version, type="Nightly")
            versionID = obj.id
        except:
            try:
                versionOBJ = project_version.objects.create(**{
                    "version": self.version,
                    "branch": "master",
                    "package_name": None,
                    "path": None,
                    "type": "Nightly",
                    "project_id": 1,
                    "status": True,
                })
            except Exception as e:
                logger.error(e)
            versionID = versionOBJ.id

        try:
            logger.info("Nightly Build Version:{}：更新配置文件".format(self.version))
            cache(id=13)
            logger.info("Nightly Build Version:{}：重启服务".format(self.version))
            Restart(id=13)
            time.sleep(300)
            createUser(server="192.168.2.103")
            logger.info("Nightly Build Version:{}：金标准测试".format(self.version))
            goldsmoke(version=versionID)
            HostObj = Server.objects.get(id=13)
            logger.info("Nightly Build Version:{}：持续化测试".format(self.version))
            durationTest(version=versionID, server=HostObj.host, aet=HostObj.remarks)
        except Exception as e:
            logger.error("Nightly Build Version：执行{0}版本冒烟失败----失败原因：{1}".format(self.version, e))


    def setFlag(self, parm):  # 外部停止线程的操作函数
        self.Flag = parm  # boolean

    def setParm(self, parm):  # 外部修改内部信息函数
        self.Parm = parm

    def getParm(self):  # 外部获得内部信息函数
        return self.count
