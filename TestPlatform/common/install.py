from .transport import SSHConnection
import threading
from django.conf import settings
from ..models import install,smoke,dictionary
import os
from ..common.gold import SmokeThread
from AutoUI.models import autoui
import logging
logger = logging.getLogger(__name__)  # 这里使用 __name__ 动态搜索定义的 logger 配置


class InstallThread(threading.Thread):
    def __init__(self, *args, **kwargs):
        threading.Thread.__init__(self)
        self.Flag = True  # 停止标志位
        # self.count = kwargs["count"]  # 可用来被外部访问的
        # 性能测试id
        self.id = kwargs["id"]
        self.obj = install.objects.get(id=self.id)
        self.ssh = SSHConnection(host=self.obj.server, pwd='biomind')
        self.dobj = dictionary.objects.get(type='install',key='oldversion')
        self.oldverion =self.dobj.value.split(',')

    def run(self):
        try:
            self.obj.type = 2
            self.obj.save()
            downssh = SSHConnection(host='192.168.2.111',pwd='P@ssw0rd2111')
            filelist = downssh.cmd("ls /lfs/nextcloud/data/hang.yin@biomind.ai/files/version/")
            for i in str(filelist,encoding="utf-8").split('\n'):
                if i not in self.oldverion and i:
                    name = i
            downpath ='/lfs/nextcloud/data/hang.yin@biomind.ai/files/version/{}'.format(name)
            path = '/files/History_version/{}/'.format(name[:-4])
            self.localpath = '/files/History_version/{0}/{1}'.format(name[:-4],name)
            if not os.path.exists(path):
                os.makedirs(path)
            downssh.download(self.localpath, downpath)
            downssh.close()
            self.obj.version = name[:-4]
            self.obj.save()
        except Exception as e:
            logger.error("下载最新版本报错{}".format(e))

    def install(self):
        try:
            self.obj.type = 3
            self.obj.save()
            path = settings.BASE_DIR
            self.ssh.upload("/home/biomind/Biomind_Test_Platform/install.sh".format(path), '/home/biomind/install.sh')
            self.ssh.upload(self.localpath,"/home/biomind/install.zip")
            self.ssh.cmd("unzip {}".format("install.zip"))
            self.ssh.cmd("bash install.sh")
        except Exception as e:
            logger.error("上传部署报错{}".format(e))

    def restart(self):
        try:
            self.obj.type = 4
            self.obj.save()
            self.ssh.cmd("sshpass -p {} biomind restart".format('biomind'))
            self.ssh.close()
        except Exception as e:
            logger.error("重启服务失败{}".format(e))

    def goldsmoke(self):
        try:
            data ={"version": self.obj.version,
                   "diseases": "44, 21, 23, 24, 30, 22, 25, 26, 31, 32, 33, 20, 19",
                   "status": True,
                   "hostid": self.obj.hosdid,
                   "thread": 1,
                   "count": 127
             }
            smokeobj = smoke.objects.create(**data)
            self.obj.type = 5
            self.obj.smokeid = smokeobj.id
            self.obj.save()
            testThread = SmokeThread(smokeobj.id)
            # 设为保护线程，主进程结束会关闭线程
            testThread.setDaemon(True)
            # 开始线程
            testThread.start()
        except Exception as e:
            logger.error("执行金标准测试报错{}".format(e))

    def UiTest(self):
        try:
            data = {"version": self.obj.version,
                    "diseases": "44, 21, 23, 24, 30, 22, 25, 26, 31, 32, 33, 20, 19",
                    "status": True,
                    "hostid": self.obj.hosdid,
                    "thread": 1,
                    "count": 127
                    }
            uobj = autoui.objects.create(**data)
            self.obj.type = 6
            self.obj.uid = uobj.id
            self.obj.save()
            # testThread = SmokeThread(smokeobj.id)
            # # 设为保护线程，主进程结束会关闭线程
            # testThread.setDaemon(True)
            # # 开始线程
            # testThread.start()
        except Exception as e:
            logger.error("执行UI自动化报错{}".format(e))

    def finish(self):
        try:
            self.obj.type = 7
            self.obj.save()
            self.dobj.value = '{},{}.zip'.format(str(self.dobj.value),self.obj.verion)
            self.dobj.save()
        except Exception as e:
            logger.error("执行UI自动化报错{}".format(e))

    def setFlag(self, parm):  # 外部停止线程的操作函数
        self.Flag = parm  # boolean

    def setParm(self, parm):  # 外部修改内部信息函数
        self.Parm = parm

    def getParm(self):  # 外部获得内部信息函数
        return self.parm

