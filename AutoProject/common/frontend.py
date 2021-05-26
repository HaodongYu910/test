import os
import time
import datetime
import logging

from .transport import SSHConnection
import threading
from django.conf import settings
from django.db.models import Count, When, Case
from ..models import install, dictionary, message_group, Server
from ..common.biomind import createUser, cache, Restart, goldsmoke, durationTest
from ..common.message import sendMessage
from ..common.loadVersion import backup
from ..common.Journal import log, AddJournal

logger = logging.getLogger(__name__)  # 这里使用 __name__ 动态搜索定义的 logger 配置

def frontend(**kwargs):
    obj = Server.objects.get(host=kwargs["host"])
    ssh = SSHConnection(host=obj.host, pwd=obj.pwd)
    try:
        ssh.cmd(
            "rclone copy -P oss://biomind-ha-se/Biomind-Viewer-Web2/{} /home/biomind/ --transfers=8".format(kwargs["version"]))
    except Exception as e:
        logger.error(e)
    try:
        ssh.cmd(
            "unzip -o {}.zip;".format(kwargs["version"]))

    except Exception as e:
        logger.error(e)
    #ssh.cmd("sshpass -p {} biomind restart;".format(obj.pwd))
