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