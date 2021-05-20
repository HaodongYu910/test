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



def deldata(server, InstallID, passwd):
    try:
        sendMessage(touser='', toparty='132', message='【安装部署】：{0} - 开始删除旧版本'.format(server))
        AddJournal(name="Installation{}".format(InstallID), content="【安装部署】：停止旧服务")
        ssh = SSHConnection(host=server, pwd=passwd)
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
        # 性能测试id
        self.id = kwargs["id"]
        self.obj = install.objects.get(id=self.id)
        self.user = self.obj.Host.user
        self.pwd = self.obj.Host.pwd
        self.ssh = SSHConnection(host=self.obj.server, pwd=self.pwd)
        self.cleanstop = ''
        self.upstop = ''
        self.restop = ''
        self.localpath = "{}/AutoProject/script/download_qa.sh".format(settings.BASE_DIR)

    # 检查磁盘大小
    def checkDisk(self):
        path = "{0}/Installation{1}.log".format(settings.LOG_PATH, self.id)
        with open(path, 'w', encoding='utf-8') as f:
            f.write("-----------Welcome Link:{}-----------\n".format(self.obj.Host.host))
        Disk = bytes.decode(self.ssh.cmd("df -h /home;"))
        size = Disk.split()[11]
        AddJournal(name="Installation{}".format(self.id), content="【磁盘空间】\n" + Disk)
        if int(size[:-1]) > 90:
            sendMessage(touser='', toparty='132', message='【注意】： {0} 磁盘空间已使用：{1}'.format(self.obj.Host.host, size))
            sendMessage(touser='', toparty='132', message='【注意】： {0} {1}'.format(self.obj.Host.host, Disk))


    def clean(self):
        self.cleanstart = time.time()
        self.installStatus(status=True, type=2)
        # 查看磁盘空间 输出日志
        self.checkDisk()
        # 删除旧的版本配置
        if self.obj.installstatus is True:
            deldata(self.obj.server, self.id, self.pwd)
        # 删除旧缓存
        try:
            self.ssh.cmd("sshpass -p {} biomind stop;".format(self.pwd))
            sendMessage(touser='', toparty='132', message='【安装部署】：（{0}）删除旧缓存'.format(self.obj.Host.host))
            AddJournal(name="Installation{}".format(self.id), content="【安装部署】：删除旧缓存\n")
            self.ssh.cmd(
                "rm -rf cache orthanc.json install.log restart.log;")
        except Exception as e:
            logger.error(e)
        # 备份原cache
        try:
            sendMessage(touser='', toparty='132', message='【安装部署】：（{0}）备份 配置文件'.format(self.obj.Host.host))
            AddJournal(name="Installation{}".format(self.id), content="【安装部署】：备份配置文件\n")

            if int(self.obj.testcase) in [1, 3]:
                cache(id=self.obj.Host_id)
            else:
                self.ssh.cmd(
                    "cp -r /home/biomind/.biomind/var/biomind/cache/ /home/biomind/cache;cp -r /home/biomind/.biomind/var/biomind/orthanc/orthanc.json /home/biomind/orthanc.json")
            self.cleanstop = time.time()
        except Exception as e:
            logger.error(e)

    def run(self):
        try:
            self.obj.starttime = datetime.datetime.now()
            self.installStatus(status=True, type=1)
            self.clean()
            self.upstart = time.time()
            # 上传安装版本
            try:
                if self.Flag is True:
                    self.installStatus(status=True, type=3)
                    logger.info('{}/AutoProject/script/install_qa.sh'.format(settings.BASE_DIR))
                    sendMessage(touser='', toparty='132', message='【安装部署】：（{0}） 下载安装版本'.format(self.obj.Host.host))
                    AddJournal(name="Installation{}".format(self.id), content="【安装部署】：rclone 下载安装版本\n")
                    self.ssh.upload('{}/AutoProject/script/install_qa.sh'.format(settings.BASE_DIR), '/home/biomind/install_qa.sh')

                    self.ssh.command("nohup sshpass -p {0} bash install_qa.sh {1} > install.log 2>&1 &".format(
                        self.obj.Host.pwd,
                        self.obj.version))
                    # 校验是否安装完成
                    while True:
                        time.sleep(60)
                        if "No such file or directory" in str(self.ssh.cmd("cd cache;")):
                            break
                        else:
                            time.sleep(15)
                self.upstop = time.time()
            except Exception as e:
                AddJournal(name="Installation{}".format(self.id), content="【安装部署】：{0}版本安装失败原因：{1}".format(self.obj.version, e))
                self.installStatus(status=False, type=3)
                return
            # 重启 服务
            self.restart()
        except Exception as e:
            self.obj.status = False
            self.obj.save()
            AddJournal(name="Installation{}".format(self.id), content="【安装部署】：安装{0}失败原因：{1}".format(self.obj.version, e))

    def restart(self):
        try:
            self.restime = time.time()
            self.installStatus(status=True, type=4)
            self.ssh.configure(self.obj.Host.host, str(self.obj.Host.protocol))
            AddJournal(name="Installation{}".format(self.id), content="【安装部署】：重启服务\n")
            sendMessage(touser='', toparty='132', message='【安装部署】：（{0}）重启服务'.format(self.obj.Host.host))
            self.ssh.command("nohup sshpass -p {} biomind restart > restart.log 2>&1 &".format(self.pwd))
            time.sleep(120)
            AddJournal(name="Installation{}".format(self.id),
                       content="【服务状态】\n" + bytes.decode(self.ssh.cmd("docker ps;")))
            self.restop = time.time()
        except:
            self.installStatus(status=False, type=4)
            return
        # 检查服务状态
        self.Judging_state()

    # 检查服务状态
    def Judging_state(self):
        try:
            b = 0
            while True:
                docker = bytes.decode(self.ssh.cmd("docker ps --format \"table {{.Names}}\t{{.RunningFor}}\t{{.Status}}\";"))
                dockerList = docker.split()
                a = 0
                for i in dockerList:
                    if i == "(healthy)":
                        a = a + 1
                if a >= 7:
                    time.sleep(30)
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
        if self.cleanstop:
            self.cleantime = "耗时：{}".format(str(round(self.cleanstop - self.cleanstart, 2)))
            if self.upstop:
                self.uptime = "耗时：{}".format(str(round(self.upstop - self.upstart, 2)))
                if self.restime:
                    self.restarttime = "耗时：{}".format(str(round(self.restop - self.restime, 2)))
                else:
                    self.restarttime = "耗时：{}".format(str(round(time.time() - self.restime, 2)))
            else:
                self.uptime = "耗时：{}".format(str(round(time.time() - self.upstart, 2)))
                self.restarttime = ''
        else:
            self.cleantime = "耗时：{}".format(str(round(time.time() - self.cleanstart, 2)))
            self.uptime = ''
            self.restarttime = ''
        return self.cleantime, self.uptime, self.restarttime


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
