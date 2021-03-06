import threading
import time
import datetime
import logging

from .transport import SSHConnection
import threading
from django.conf import settings
from ..models import install, project_version, Server
from ..common.message import sendMessage
from ..common.Journal import log, AddJournal

logger = logging.getLogger(__name__)  # 这里使用 __name__ 动态搜索定义的 logger 配置


class InstallThread(threading.Thread):
    def __init__(self, **kwargs):
        threading.Thread.__init__(self)
        self.Flag = True  # 停止标志位
        # 性能测试id
        self.id = kwargs["id"]
        self.obj = install.objects.get(id=self.id)
        self.versionObj = project_version.objects.get(id=self.obj.version)
        self.user = self.obj.Host.user
        self.pwd = self.obj.Host.pwd
        self.ssh = SSHConnection(host=self.obj.server, pwd=self.pwd)
        self.localpath = "{}/AutoProject/script/download_qa.sh".format(settings.BASE_DIR)
        self.cacheTag = ''
        self.reset = "n"

    def Reset(self):
        self.reset = "y"
        try:
            logger.info("删除开始")
            sendMessage(touser='', toparty='132', message='【安装部署】： - 开始删除旧版本')
            AddJournal(name="Installation{}".format(self.id), content="【安装部署】：停止旧服务，删除旧版本")
            self.ssh.cmd(f"sshpass -p {self.pwd} biomind stop;")
            self.ssh.shcmd("sshpass -p y docker system prune")
            self.ssh.cmd("docker rmi -f $(docker images -qa);docker volume rm $(docker volume ls -q)")
            self.ssh.cmd(f"sshpass -p {self.pwd} sudo rm -rf /lfs/biomind;")
            self.ssh.cmd(f"sshpass -p {self.pwd} sudo rm -rf /lfs/Biomind-3Dserver;")
            self.ssh.cmd(f"sshpass -p {self.pwd} sudo rm -rf /home/biomind/.biomind;")
            self.ssh.cmd(f"sshpass -p {self.pwd} sudo rm -rf /home/biomind/.3D-biomind;")
            self.ssh.cmd(
                f"sshpass -p {self.pwd} sudo rpm -e supervisor;sshpass -p {self.pwd} sudo rm -rf /etc/yum.repos.d/3dlocal.repo")
            AddJournal(name="Installation{}".format(self.id), content="【安装部署】: 删除完成")
            sendMessage(touser='', toparty='132', message='【安装部署】：删除完成')

        except Exception as e:
            sendMessage(touser='', toparty='132', message='【安装部署】：{0} - 删除报错:{1}'.format(self.id, e))
            logger.error("【安装部署】：删除旧的版本失败：{}".format(e))


    def checkDisk(self):
        self.installStatus(status=True, type=2)
        try:
            sendMessage(touser='', toparty='132', message='【安装部署】：（{0}）安装部署开始'.format(self.obj.Host.host))
            AddJournal(name="Installation{}".format(self.id), content="【安装部署】：删除旧缓存\n")
            self.ssh.cmd(
                "rm -rf cache orthanc.json install.log restart.log;")
        except Exception as e:
            logger.error(e)
        # 查看磁盘空间 输出日志
        path = "{0}/Installation{1}.log".format(settings.LOG_PATH, self.id)
        with open(path, 'w', encoding='utf-8') as f:
            f.write("-----------{} Install version-----------\n".format(self.obj.Host.host))
        try:
            Disk = bytes.decode(self.ssh.cmd("df -h /home;"))
            AddJournal(name="Installation{}".format(self.id), content="【磁盘空间】\n" + Disk)
            size = Disk.split()[11]
            if int(size[:-1]) > 90:
                sendMessage(touser='', toparty='132', message='【注意】： {0} 磁盘空间已使用：{1}'.format(self.obj.Host.host, size))
                sendMessage(touser='', toparty='132', message='【注意】： {0} {1}'.format(self.obj.Host.host, Disk))
            if self.obj.installstatus is True:
                self.Reset()
        except Exception as e:
            logger.error(e)

    def run(self):
        try:
            self.installStatus(status=True, type=1)
            self.obj.starttime = datetime.datetime.now()
            self.checkDisk()
            # 上传安装版本
            try:
                if self.Flag is True:
                    self.installStatus(status=True, type=3)
                    #
                    # self.ssh.upload(f'{settings.BASE_DIR}/AutoProject/script/install_qa.sh',
                    #                 '/home/biomind/install_qa.sh')
                    AddJournal(name="Installation{}".format(self.id), content="【安装部署】：rclone 下载安装版本\n")

                    self.ssh.command(
                        "sshpass -p {0} bash /home/biomind/install_qa.sh {1} {2} {3} {4} {5}> install.log 2>&1".format(
                            self.pwd,
                            str(self.versionObj.version),
                            str(self.versionObj.package_name),
                            self.versionObj.path,
                            self.pwd,
                            self.reset
                        ))
                    logger.info("安装完成")
            except Exception as e:
                AddJournal(name="Installation{}".format(self.id),
                           content="【安装部署】：{0}版本安装失败原因：{1}".format(self.versionObj.version, e))
                self.installStatus(status=False, type=3)
                return
            # 重启 服务
            self.restart()
        except Exception as e:
            self.obj.status = False
            self.obj.save()
            logger.error(e)
            AddJournal(name="Installation{}".format(self.id),
                       content="【安装部署】：安装{0}失败原因：{1}".format(self.versionObj.version, e))


    def restart(self):
        try:
            self.installStatus(status=True, type=4)
            if self.reset == "y":
                self.ssh.configure(self.obj.Host.host, str(self.obj.Host.protocol))
            AddJournal(name="Installation{}".format(self.id), content="【安装部署】：重启服务\n")
            sendMessage(touser='', toparty='132', message='【安装部署】：（{0}）安装完成，重启服务中'.format(self.obj.Host.host))
            self.ssh.command("nohup sshpass -p {} biomind restart > restart.log 2>&1 &".format(self.pwd))
            time.sleep(120)
            AddJournal(name="Installation{}".format(self.id),
                       content="【服务状态】\n" + bytes.decode(self.ssh.cmd("docker ps;")))
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
                docker = bytes.decode(
                    self.ssh.cmd("docker ps --format \"table {{.Names}}\t{{.RunningFor}}\t{{.Status}}\";"))
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
                    self.installStatus(status=False, type=5)
                    sendMessage(touser='', toparty='132', message='【安装部署】：（{0}）安装部署完成'.format(self.obj.Host.host))
                    AddJournal(name="Installation{}".format(self.id), content="【安装部署】：安装完成\n")

                    if self.obj.smokeid == 0:
                        AddJournal(name="Installation{}".format(self.id), content="【安装部署】：执行金标准测试\n")
                        goldsmoke(version=self.versionObj.version)
                    if self.obj.uid == 0:
                        goldsmoke(version=self.versionObj.version)

                    return True
                elif b == 10:
                    self.installStatus(status=False, type=5)
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
                       content="【安装部署】：安装{0}失败原因：{1}".format(self.versionObj.version, e))
            return False

    # 变更状态
    def installStatus(self, status, type):
        self.obj.status = status
        self.obj.type = type
        self.obj.save()