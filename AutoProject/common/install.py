from .transport import SSHConnection
import threading
from django.conf import settings
from django.db.models import Count, When, Case
from ..models import install, dictionary
from AutoInterface.models import gold_test, gold_record
import os
from AutoInterface.common.gold import GoldThread
from AutoUI.models import autoui, auto_uirecord
import time
import datetime
import logging
from ..utils.keycloak.keycloakadmin import KeycloakAdm
from ..common.message import sendMessage
from ..common.biomind import RestartThread
from ..common.loadVersion import backup
from ..common.Journal import log, AddJournal

logger = logging.getLogger(__name__)  # 这里使用 __name__ 动态搜索定义的 logger 配置


def deldata(server, InstallID, passwd):
    try:
        sendMessage(touser='', toparty='132', message='【安装部署】：{0} - 开始删除旧版本'.format(server))
        AddJournal("Installation{}".format(InstallID), "【安装部署】：停止旧服务")
        ssh = SSHConnection(host=server, pwd=passwd)
        ssh.cmd("sshpass -p {} biomind stop".format(passwd))
        ssh.shcmd("sshpass -p y docker system prune")
        AddJournal("Installation{}".format(InstallID), "【安装部署】：docker system prune")
        ssh.cmd("docker volume rm $(docker volume ls -q)")
        AddJournal("Installation{}".format(InstallID), "【安装部署】：docker volume rm $(docker volume ls -q)")
        ssh.cmd("sshpass -p {} sudo rm -rf /lfs/biomind".format(passwd))
        AddJournal("Installation{}".format(InstallID), "【安装部署】：删除/lfs/biomind")
        ssh.cmd("sshpass -p {} sudo rm -rf /lfs/Biomind-3Dserver".format(passwd))
        AddJournal("Installation{}".format(InstallID), "【安装部署】：删除 Biomind-3Dserver")
        ssh.cmd("sshpass -p {} sudo rm -rf /home/biomind/.biomind".format(passwd))
        AddJournal("Installation{}".format(InstallID), "【安装部署】：删除 .biomind")
        ssh.cmd("sshpass -p {} sudo rm -rf /home/biomind/.3D-biomind".format(passwd))
        AddJournal("Installation{}".format(InstallID), "【安装部署】: 删除 .3D-biomind")
        ssh.cmd("sshpass -p {} sudo rpm -e supervisor".format(passwd))
        AddJournal("Installation{}".format(InstallID), "【安装部署】: 删除 supervisor")
        ssh.cmd("sshpass -p {} sudo rm -rf /etc/yum.repos.d/3dlocal.repo".format(passwd))
        sendMessage(touser='', toparty='132', message='【安装部署】：{0} - 删除完成'.format(server))
    except Exception as e:
        sendMessage(touser='', toparty='132', message='【安装部署】：{0} - 删除报错请查看日志'.format(server))
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
        path = "{0}/Installation{2}.log".format(settings.LOG_PATH, self.id)
        with open(path, 'w', encoding='utf-8') as f:
            f.write("""------【部署安装-日志信息】------""")

    def run(self):
        try:
            self.obj.starttime = datetime.datetime.now()
            self.installStatus(status=True, type=1)
            # 查看磁盘空间 输出日志
            AddJournal("Installation{}".format(self.id), """【磁盘空间】""" + bytes.decode(self.ssh.cmd("df -h;")))
            # 删除旧的版本配置
            if self.obj.installstatus is True:
                deldata(self.obj.server, self.id, self.pwd)
            # 判断是否下载版本安装包
            try:
                if self.obj.version:
                    self.localpath = '/files/History_version/{0}/{1}.zip'.format(self.obj.version, self.obj.version)
                    if not os.path.exists(self.localpath):
                        AddJournal("Installation{}".format(self.id), "【安装部署】：下载备份安装包")
                        load = backup(version=self.obj.version)
                    elif self.obj.testcase == 0:
                        AddJournal("Installation{}".format(self.id), "【安装部署】：下载备份安装包")
                        load = backup(version=self.obj.version)
                else:
                    load = backup(version="")
                if load is True:
                    self.installStatus(status=True, type=2)
                else:
                    self.installStatus(status=False, type=2)
                    return
            except Exception as e:
                AddJournal("Installation{}".format(self.id), "【安装部署】：下载安装包失败原因：{}".format(e))
                self.installStatus(status=False, type=2)
                return
            # 上传服务器安装包
            try:
                if self.Flag is True:
                    self.installStatus(status=True, type=3)
                    sendMessage(touser='', toparty='132', message='【安装部署】：（{0}）上传最新安装包'.format(self.obj.Host.host))
                    AddJournal("Installation{}".format(self.id), "【安装部署】：上传安装包")
                    self.ssh.upload(self.localpath, "/home/biomind/QaInstall.zip")
                    self.ssh.cmd("sshpass -p {0} sudo rm -rf {1}/".format(self.pwd, self.obj.version))
                    sendMessage(touser='', toparty='132', message='【安装部署】：（{0}）解压安装包'.format(self.obj.Host.host))
                    AddJournal("Installation{}".format(self.id), "【安装部署】：解压安装包")
                    self.ssh.cmd("unzip {}".format("QaInstall.zip"))
            except Exception as e:
                AddJournal("Installation{}".format(self.id), "【安装部署】：上传{0}版本安装包失败原因：{1}".format(self.obj.version, e))
                self.installStatus(status=False, type=3)
                return
            try:
                if self.Flag is True:
                    AddJournal("Installation{}".format(self.id), "【安装部署】：停止旧服务 & 安装新版本")
                    self.ssh.cmd("sshpass -p {} biomind stop;".format(self.pwd))
                    self.ssh.cmd("cd {0};sshpass -p {1} bash setup_engine.sh;".format(self.obj.version, self.pwd))
                    time.sleep(300)
            except Exception as e:
                AddJournal("Installation{}".format(self.id), "【安装部署】：安装{0}版本安装包失败原因：{1}".format(self.obj.version, e))
                self.installStatus(status=False, type=3)
                return

            try:
                sendMessage(touser='', toparty='132', message='【安装部署】：（{0}）更新 配置文件'.format(self.obj.Host.host))
                AddJournal("Installation{}".format(self.id), "【安装部署】：备份更新配置文件")
                self.ssh.upload("/files1/classifier/orthanc.json",
                                "/home/biomind/.biomind/var/biomind/orthanc/orthanc.json")
                self.ssh.upload("/files1/classifier/cache.zip",
                                "/home/biomind/cache.zip")
                self.ssh.cmd(
                    "mv /home/biomind/.biomind/var/biomind/cache cachebak;unzip -o cache.zip -d /home/biomind/.biomind/var/biomind/;")

            except Exception as e:
                AddJournal("Installation{}".format(self.id), "【安装部署】：安装{0}版本更新文件失败原因：{1}".format(self.obj.version, e))
                self.installStatus(status=False, type=3)
                return
            try:
                self.installStatus(status=True, type=4)
                AddJournal("Installation{}".format(self.id), "【安装部署】：重启服务")
                sendMessage(touser='', toparty='132', message='【安装部署】：（{0}）重启服务'.format(self.obj.Host.host))
                restart = RestartThread(id=self.obj.Host_id)
                restart.setDaemon(True)
                # 开始线程
                restart.start()
                time.sleep(300)
                AddJournal("Installation{}".format(self.id), """"【服务状态】""" + bytes.decode(self.ssh.cmd("docker -ps;")))
            except:
                self.installStatus(status=False, type=4)
                return

            self.createUser()
            self.installStatus(status=True, type=5)
            sendMessage(touser='', toparty='132', message='【安装部署】：（{0}）安装部署完成'.format(self.obj.Host.host))
            AddJournal("Installation{}".format(self.id), "【安装部署】：安装完成")
            restart.setFlag = False
            if self.obj.smokeid == 0:
                self.goldsmoke()
                self.installStatus(status=False, type=6)
            if self.obj.uid == 0:
                self.UiTest()
                self.installStatus(status=False, type=7)
        except Exception as e:
            self.obj.status = False
            self.obj.save()
            AddJournal("Installation{}".format(self.id), "【安装部署】：安装{0}失败原因：{1}".format(self.obj.version, e))

    def createUser(self):
        try:
            AddJournal("Installation{}".format(self.id), "【安装部署】：创建 3D 用户")
            user_info = {"username": "biomind3d", "enabled": True,
                         "credentials": [{"value": "engine3D.", "type": "password", }]}
            kc_adm = KeycloakAdm(orthanc_ip='{0}://{1}'.format(self.obj.Host.protocol, self.obj.Host.host))
            kc_adm.create_update_user_add_all_group(user_info)
        except Exception as e:
            AddJournal("Installation{}".format(self.id), "【安装部署】：Failed to create User: {e}".format(e))
            self.installStatus(status=False, type=5)
            return

    def goldsmoke(self):
        try:
            if self.Flag is True:
                sendMessage(touser='', toparty='132', message='【安装部署】：（{0}）创建金标准测试'.format(self.obj.Host.host))
                data = {"version": self.obj.version,
                        "diseases": "19,44,31,32,21,33,23,24,20,30,22,25,26",
                        "status": True,
                        "Host_id": int(self.obj.Host_id),
                        "thread": 3,
                        "count": 118
                        }
                AddJournal("Installation{}".format(self.id), "【安装部署】：创建执行金标准测试")

                smokeObj = gold_test.objects.create(**data)
                self.obj.smokeid = smokeObj.id
                self.obj.save()
                testThread = GoldThread(smokeObj.id)
                # 设为保护线程，主进程结束会关闭线程
                testThread.setDaemon(True)
                # 开始线程
                testThread.start()
        except Exception as e:
            self.installStatus(status=False, type=6)
            AddJournal("Installation{}".format(self.id), "【安装部署】：执行金标准测试报错: {e}".format(e))

    def UiTest(self):
        try:
            if self.Flag is True:
                data = {"version": self.obj.version,
                        "setup": "1",
                        "cases": "1",
                        "tearDown": "1",
                        "status": True,
                        "hostid": self.obj.hostid,
                        "thread": 1
                        }
                AddJournal("Installation{}".format(self.id), "【安装部署】：创建执行UI测试")

                uiObj = autoui.objects.create(**data)
                self.obj.type = 7
                self.obj.uid = uiObj.id
                self.obj.save()
                # testThread = GoldThread(smokeobj.id)
                # # 设为保护线程，主进程结束会关闭线程
                # testThread.setDaemon(True)
                # # 开始线程
                # testThread.start()
        except Exception as e:
            self.installStatus(status=False, type=7)
            AddJournal("Installation{}".format(self.id), "【安装部署】：执行UI测试报错: {e}".format(e))

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
