import os
import time
import datetime
import logging

from .transport import SSHConnection
import threading
from django.conf import settings
from django.db.models import Count, When, Case
from ..models import install, dictionary, message_group, Server
from AutoInterface.models import gold_test, gold_record
from AutoInterface.common.gold import GoldThread
from AutoUI.models import autoui, auto_uirecord

from ..common.biomind import createUser, cache, Restart, goldsmoke, durationTest
from ..common.message import sendMessage
from ..common.loadVersion import backup
from ..common.Journal import log, AddJournal

logger = logging.getLogger(__name__)  # 这里使用 __name__ 动态搜索定义的 logger 配置



def deldata(server, InstallID, passwd):
    try:
        sendMessage(touser='', toparty='132', message='【安装部署】：{0} - 开始删除旧版本'.format(server))
        AddJournal(name="Installation{}".format(InstallID), content="【安装部署】：停止旧服务")
        ssh = SSHConnection(host=server, pwd=passwd)
        ssh.cmd("sshpass -p {} biomind stop".format(passwd))
        ssh.shcmd("sshpass -p y docker system prune")
        AddJournal(name="Installation{}".format(InstallID), content="【安装部署】：docker system prune")
        ssh.cmd("docker volume rm $(docker volume ls -q)")
        AddJournal(name="Installation{}".format(InstallID), content="【安装部署】：docker volume rm $(docker volume ls -q)")
        ssh.cmd("sshpass -p {} sudo rm -rf /lfs/biomind".format(passwd))
        AddJournal(name="Installation{}".format(InstallID), content="【安装部署】：删除/lfs/biomind")
        ssh.cmd("sshpass -p {} sudo rm -rf /lfs/Biomind-3Dserver".format(passwd))
        AddJournal(name="Installation{}".format(InstallID), content="【安装部署】：删除 Biomind-3Dserver")
        ssh.cmd("sshpass -p {} sudo rm -rf /home/biomind/.biomind".format(passwd))
        AddJournal(name="Installation{}".format(InstallID), content="【安装部署】：删除 .biomind")
        ssh.cmd("sshpass -p {} sudo rm -rf /home/biomind/.3D-biomind".format(passwd))
        AddJournal(name="Installation{}".format(InstallID), content="【安装部署】: 删除 .3D-biomind")
        ssh.cmd("sshpass -p {} sudo rpm -e supervisor".format(passwd))
        AddJournal(name="Installation{}".format(InstallID), content="【安装部署】: 删除 supervisor")
        ssh.cmd("sshpass -p {} sudo rm -rf /etc/yum.repos.d/3dlocal.repo".format(passwd))
        sendMessage(touser='', toparty='132', message='【安装部署】：{0} - 删除完成'.format(server))
    except Exception as e:
        sendMessage(touser='', toparty='132', message='【安装部署】：{0} - 删除报错:{1}'.format(server, e))
        logger.error("【安装部署】：删除旧的版本失败：{}".format(e))



class InstallThread(threading.Thread):
    def __init__(self, **kwargs):
        threading.Thread.__init__(self)
        self.Flag = True  # 停止标志位
        # self.count = kwargs["count"]  # 可用来被外部访问的
        # 性能测试id
        self.id = kwargs["id"]
        self.obj = install.objects.get(id=self.id)
        self.user = self.obj.Host.user
        self.pwd = self.obj.Host.pwd
        self.ssh = SSHConnection(host=self.obj.server, pwd=self.pwd)
        path = "{0}/Installation{1}.log".format(settings.LOG_PATH, self.id)
        with open(path, 'w', encoding='utf-8') as f:
            f.write("-----------Welcome Link:{}-----------\n".format(self.obj.Host.host))
    # 检查磁盘大小
    def checkDisk(self):
        Disk = bytes.decode(self.ssh.cmd("df -h /home;"))
        size = Disk.split()[11]
        AddJournal(name="Installation{}".format(self.id), content="【磁盘空间】\n" + Disk)
        if int(size[:-1]) > 90:
            sendMessage(touser='', toparty='132', message='【注意】： {0} 磁盘空间已使用：{1}'.format(self.obj.Host.host, size))
            sendMessage(touser='', toparty='132', message='【注意】： {0} {1}'.format(self.obj.Host.host, Disk))

    def run(self):
        try:
            self.obj.starttime = datetime.datetime.now()
            self.installStatus(status=True, type=1)
            # 查看磁盘空间 输出日志
            self.checkDisk()
            # 删除旧的版本配置
            if self.obj.installstatus is True:
                deldata(self.obj.server, self.id, self.pwd)
            # 判断是否下载版本安装包
            try:
                load = True
                if self.obj.version:
                    self.localpath = '/files/History_version/{0}/{1}.zip'.format(self.obj.version, self.obj.version)
                    if not os.path.exists(self.localpath):
                        AddJournal(name="Installation{}".format(self.id), content="【安装部署】：下载备份安装包\n")
                        load = backup(version=self.obj.version)
                    elif int(self.obj.testcase) in [0, 3]:
                        AddJournal(name="Installation{}".format(self.id), content="【安装部署】：下载备份安装包\n")
                        load = backup(version=self.obj.version)
                else:
                    load = backup(version="")
                if load is True:
                    self.installStatus(status=True, type=2)
                else:
                    self.installStatus(status=False, type=2)
                    return
            except Exception as e:
                AddJournal(name="Installation{}".format(self.id), content="【安装部署】：下载安装包失败原因：{}".format(e))
                self.installStatus(status=False, type=2)
                return
            # 上传服务器安装包
            try:
                if self.Flag is True:
                    self.installStatus(status=True, type=3)
                    sendMessage(touser='', toparty='132', message='【安装部署】：（{0}）上传最新安装包'.format(self.obj.Host.host))
                    AddJournal(name="Installation{}".format(self.id), content="【安装部署】：上传安装包\n")
                    self.ssh.upload(self.localpath, "/home/biomind/QaInstall.zip")
                    self.ssh.cmd("sshpass -p {0} sudo rm -rf {1}/ install.log restart.log".format(self.pwd, self.obj.version))
                    sendMessage(touser='', toparty='132', message='【安装部署】：（{0}）解压安装包'.format(self.obj.Host.host))
                    AddJournal(name="Installation{}".format(self.id), content="【安装部署】：解压安装包\n")
                    self.ssh.command("unzip -o QaInstall.zip")

            except Exception as e:
                AddJournal(name="Installation{}".format(self.id), content="【安装部署】：{0}版本安装包 失败原因：{1}".format(self.obj.version, e))
                self.installStatus(status=False, type=3)
                return
            # 安装版本
            try:
                if self.Flag is True:
                    AddJournal(name="Installation{}".format(self.id), content="【安装部署】：停止旧服务 & 安装新版本\n")
                    self.ssh.cmd("sshpass -p {} biomind stop;".format(self.pwd))
                    self.ssh.command("cd {0};nohup sshpass -p {1} bash setup_engine.sh > install.log 2>&1 &".format(self.obj.version, self.pwd))
                    while True:
                        time.sleep(120)
                        result = bytes.decode(self.ssh.cmd(
                            "ls /home/biomind/.biomind/lib/versions/{}/deps/Biomind-Management/".format(
                                self.obj.version)))
                        if ('build' in result) is True:
                            time.sleep(60)
                            break
                        else:
                            time.sleep(30)

            except Exception as e:
                AddJournal(name="Installation{}".format(self.id), content="【安装部署】：安装{0}版本安装包失败原因：{1}".format(self.obj.version, e))
                self.installStatus(status=False, type=3)
                return

            try:
                if int(self.obj.testcase) in [1, 3]:
                    sendMessage(touser='', toparty='132', message='【安装部署】：（{0}）更新 配置文件'.format(self.obj.Host.host))
                    AddJournal(name="Installation{}".format(self.id), content="【安装部署】：备份更新配置文件\n")
                    cache(id=self.obj.Host_id)
            except Exception as e:
                AddJournal(name="Installation{}".format(self.id), content="【安装部署】：安装{0}版本更新文件失败原因：{1}".format(self.obj.version, e))
                self.installStatus(status=False, type=3)
                return
            try:
                self.installStatus(status=True, type=4)
                self.ssh.configure(self.obj.Host.host, str(self.obj.Host.protocol))
                AddJournal(name="Installation{}".format(self.id), content="【安装部署】：重启服务\n")
                sendMessage(touser='', toparty='132', message='【安装部署】：（{0}）重启服务'.format(self.obj.Host.host))
                self.ssh.command("nohup sshpass -p {} biomind restart > restart.log 2>&1 &".format(self.pwd))
                time.sleep(120)
                AddJournal(name="Installation{}".format(self.id), content="【服务状态】\n" + bytes.decode(self.ssh.cmd("docker ps;")))
            except:
                self.installStatus(status=False, type=4)
                return
            # 检查服务状态
            self.Judging_state()

        except Exception as e:
            self.obj.status = False
            self.obj.save()
            AddJournal(name="Installation{}".format(self.id), content="【安装部署】：安装{0}失败原因：{1}".format(self.obj.version, e))

    # 检查服务状态
    def Judging_state(self):
        try:
            b = 0
            while True:
                docker = bytes.decode(self.ssh.cmd("docker ps;"))
                dockerList = docker.split()
                a = 0
                for i in dockerList:
                    if i == "(healthy)":
                        a = a + 1
                if a >= 9:
                    AddJournal(name="Installation{}".format(self.id), content="【安装部署】：createUser \n")
                    createUser(user="biomind3d", pwd="engine3D.", protocol=self.obj.Host.protocol,
                               server=self.obj.Host.host)
                    self.installStatus(status=True, type=5)
                    sendMessage(touser='', toparty='132', message='【安装部署】：（{0}）安装部署完成'.format(self.obj.Host.host))
                    AddJournal(name="Installation{}".format(self.id), content="【安装部署】：安装完成\n")

                    if self.obj.smokeid == 0:
                        AddJournal(name="Installation{}".format(self.id), content="【安装部署】：执行金标准测试\n")
                        goldsmoke(version=self.obj.version)
                        self.installStatus(status=False, type=6)
                    if self.obj.uid == 0:
                        goldsmoke(version=self.obj.version)
                        self.installStatus(status=False, type=7)

                    return True
                elif b == 10:
                    sendMessage(touser='', toparty='132', message='【注意】：（{0}）安装部署可能失败请看下'.format(self.obj.Host.host))
                    AddJournal(name="Installation{}".format(self.id), content="【安装部署】：安装部署可能失败请看下\n")
                    return False
                else:
                    time.sleep(30)
                    b = b + 1

        except Exception as e:
            self.obj.status = False
            self.obj.save()
            AddJournal(name="Installation{}".format(self.id),
                       content="【安装部署】：安装{0}失败原因：{1}".format(self.obj.version, e))
            return False
    # 变更状态
    def installStatus(self, status, type):
        self.obj.status = status
        self.obj.type = type
        self.obj.save()

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
