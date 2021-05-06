import os
import time
import datetime
import logging


from AutoProject.common.transport import SSHConnection
import threading
from django.conf import settings
from django.db.models import Count, When, Case
from ..models import install, dictionary, message_group, Server

logger = logging.getLogger(__name__)  # 这里使用 __name__ 动态搜索定义的 logger 配置


class MonitorThread(threading.Thread):
    def __init__(self, **kwargs):
        threading.Thread.__init__(self)
        self.Flag = True  # 停止标志位
        # self.count = kwargs["count"]  # 可用来被外部访问的
        # 性能测试id
        self.obj = Server.objects.get(id=kwargs["id"])
        self.user = self.obj.Host.user
        self.pwd = self.obj.Host.pwd
        self.ssh = SSHConnection(host=self.obj.server, pwd=self.pwd)

        self.ssh.cmd("wget https://ifileserver.biomind.com.cn/index.php/s/4dMqo7F2meb4cTp/download -O ./monitor.zip --no-check-certificate;unzip ./monitor.zip;")

    def run(self):
        try:
            pass
        except Exception as e:
            logger.error(e)

    def GPUInstall(self):
        try:
            self.ssh.cmd()
        except Exception as e:
            logger.error(e)


    def run(self):
        try:
            pass
        except Exception as e:
            logger.error(e)


    def run(self):
        try:
            pass
        except Exception as e:
            logger.error(e)



    def installStatus(self, status, type):
        pass

    def setFlag(self, parm):  # 外部停止线程的操作函数
        self.Flag = parm  # boolean

    def setParm(self, parm):  # 外部修改内部信息函数
        self.Parm = parm

    def getParm(self):  # 外部获得内部信息函数
        return self.parm


class smokeThread(threading.Thread):
    def __init__(self, **kwargs):
        threading.Thread.__init__(self)
        self.Flag = True  # 停止标志位
        # 版本号
        self.version = kwargs["version"]
        self.server = Server.objects.get(id='13')


    def run(self):
        try:
            logger.info("Nightly Build Version:{}：更新配置文件".format(self.version))
            cache(id=self.server.id)

            logger.info("Nightly Build Version:{}：重启服务".format(self.version))
            Restart(id=self.server.id)
            time.sleep(100)

            logger.info("Nightly Build Version:{}：金标准测试".format(self.version))
            goldsmoke(version=self.version)

            logger.info("Nightly Build Version:{}：持续化测试".format(self.version))
            durationTest(version=self.version, server=self.server.host, aet=self.server.remarks)
        except Exception as e:
            logger.error("Nightly Build Version：执行{0}版本冒烟失败----失败原因：{1}".format(self.obj.version, e))

    def setFlag(self, parm):  # 外部停止线程的操作函数
        self.Flag = parm  # boolean

