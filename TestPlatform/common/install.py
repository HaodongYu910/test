from .transport import SSHConnection
import threading
from django.conf import settings
from ..models import install



class InstallThread(threading.Thread):
    def __init__(self, *args, **kwargs):
        threading.Thread.__init__(self)
        self.Flag = True  # 停止标志位
        # self.count = kwargs["count"]  # 可用来被外部访问的
        # 性能测试id
        self.id = kwargs["id"]
        self.obj = install.objects.get(id=self.id)


    def download(self):
        ssh = SSHConnection(host='192.168.2.111',pwd='P@ssw0rd2111')
        ssh.cmd("unzip {}".format('zipname'))
        name =''
        downpath ='/lfs/nextcloud/data/hang.yin@biomind.ai/files/'.format(name)
        ssh.download('/home/biomind/{}'.format(name), downpath)
        ssh.cmd("unzip {}".format(name))
        ssh.close()
        return name

    def install(self, host, pwd, name):
        ssh = SSHConnection(host=host, pwd=pwd)
        path = settings.BASE_DIR
        ssh.upload("{}/test.sh".format(path), '/home/biomind/test.sh')
        ssh.cmd("bash test.sh")
        ssh.cmd("sshpass -p {} biomind restart".format('biomind'))
        ssh.close()

    def UiTest(self,host, pwd,name):
        print(1)

    def goldsmoke(self,host, pwd,name):
        print(1)

    def setFlag(self, parm):  # 外部停止线程的操作函数
        self.Flag = parm  # boolean

    def setParm(self, parm):  # 外部修改内部信息函数
        self.Parm = parm

    def getParm(self):  # 外部获得内部信息函数
        return self.parm

