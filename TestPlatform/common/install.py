from .transport import SSHConnection
import threading
from django.conf import settings
from django.db.models import Count, When, Case
from ..models import install, smoke, dictionary, smoke_record, base_data
import os
from ..common.gold import SmokeThread
from AutoUI.models import autoui, auto_uirecord
import logging
import time, datetime

logger = logging.getLogger(__name__)  # 这里使用 __name__ 动态搜索定义的 logger 配置


def deldata(server):
    ssh = SSHConnection(host=server, pwd='biomind')
    ssh.cmd("sshpass -p biomind biomind stop")
    ssh.cmd("sshpass -p y docker system prune")
    ssh.cmd("docker volume rm $(docker volume ls -q)")
    ssh.cmd("sshpass -p biomind sudo rm -rf /lfs/biomind")
    ssh.cmd("sshpass -p biomind sudo rm -rf /lfs/Biomind-3Dserver")
    ssh.cmd("sshpass -p biomind sudo rm -rf /home/biomind/.biomind")
    ssh.cmd("sshpass -p biomind sudo rm -rf /home/biomind/.3D-biomind")
    ssh.cmd("sshpass -p biomind sudo rpm -e supervisor")
    ssh.cmd("sshpass -p biomind sudo rm -rf /etc/yum.repos.d/3dlocal.repo")



class InstallThread(threading.Thread):
    def __init__(self, **kwargs):
        threading.Thread.__init__(self)
        self.Flag = True  # 停止标志位
        # self.count = kwargs["count"]  # 可用来被外部访问的
        # 性能测试id
        self.id = kwargs["id"]
        self.obj = install.objects.get(id=self.id)
        self.ssh = SSHConnection(host=self.obj.server, pwd='biomind')
        self.dobj = dictionary.objects.get(type='install', key='oldversion')
        self.oldversion = self.dobj.value.split(',')

    def run(self):
        try:
            self.obj.status =True
            self.obj.type = 2
            self.obj.save()
            if self.obj.installstatus is True:
                deldata(self.obj.server)
            downssh = SSHConnection(host='192.168.2.111', pwd='P@ssw0rd2111')
            if self.obj.version:
                self.localpath = '/files/History_version/{0}/{1}.zip'.format(self.obj.version, self.obj.version)
                if not os.path.exists(self.localpath):
                    downpath = '/lfs/nextcloud/data/mengyue.he@biomind.ai/files/Version_for_QA/{0}/{1}.zip'.format(
                        self.obj.version,self.obj.version)
                    path = '/files/History_version/{0}'.format(self.obj.version)
                    if not os.path.exists(path):
                        os.makedirs(path)
                    downssh.download(self.localpath, downpath)
                    downssh.close()
            else:
                filelist = downssh.cmd("ls /lfs/nextcloud/data/mengyue.he@biomind.ai/files/Version_for_QA/")
                for i in str(filelist, encoding="utf-8").split('\n'):
                    if i not in self.oldversion and i:
                        name = i
                downpath = '/lfs/nextcloud/data/mengyue.he@biomind.ai/files/Version_for_QA/{}'.format(name)
                path = '/files/History_version/{}/'.format(name[:-4])
                self.localpath = '/files/History_version/{0}/{1}'.format(name[:-4], name)
                if not os.path.exists(path):
                    os.makedirs(path)
                downssh.download(self.localpath, downpath)
                downssh.close()
                self.obj.version = name[:-4]
                self.obj.save()
        except Exception as e:
            self.obj.status = False
            self.obj.save()
            logger.error("下载最新版本报错{}".format(e))

        # def install(self):
        try:
            self.obj.type = 3
            self.obj.save()
            if not os.path.exists("/home/biomind/{}".format(self.obj.version)):
                self.ssh.upload(self.localpath, "/home/biomind/QaInstall.zip")
                self.ssh.cmd("unzip {}".format("QaInstall.zip"))
            self.ssh.cmd("sshpass -p biomind biomind stop;")
            logger.info("biomind stop")
            self.ssh.cmd("cd {};sshpass -p biomind bash setup_engine.sh;".format(self.obj.version))
            logger.info("biomind bash setup_engine.sh")
        except Exception as e:
            self.obj.status = False
            self.obj.save()
            logger.error("上传部署报错{}".format(e))

        # def restart(self):
        try:
            self.obj.type = 4
            self.obj.save()
            self.ssh.cmd("sshpass -p biomind biomind restart")
            self.ssh.close()
            time.sleep(600)
        except Exception as e:
            self.obj.status = False
            self.obj.save()
            logger.error("重启服务失败{}".format(e))

        # def goldsmoke(self):
        try:
            data = {"version": self.obj.version,
                    "diseases": "44, 21, 23, 24, 30, 22, 25, 26, 31, 32, 33, 20, 19",
                    "status": True,
                    "hostid": self.obj.hosdid,
                    "thread": 1,
                    "count": 127
                    }
            smokeobj = smoke.objects.create(**data)
            self.obj.status = False
            self.obj.type = 5
            self.obj.smokeid = smokeobj.id
            self.obj.save()
            testThread = SmokeThread(smokeobj.id)
            # 设为保护线程，主进程结束会关闭线程
            testThread.setDaemon(True)
            # 开始线程
            testThread.start()
        except Exception as e:
            self.obj.status = False
            self.obj.save()
            logger.error("执行金标准测试报错{}".format(e))

        # def UiTest(self):

        try:
            data = {"version": self.obj.version,
                    "setup": "1",
                    "cases": "1",
                    "tearDown": "1",
                    "status": True,
                    "hostid": self.obj.hosdid,
                    "thread": 1
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
            self.obj.status = False
            self.obj.save()
            logger.error("执行UI自动化报错{}".format(e))

        # def finish(self):
        try:
            self.obj.starttime = datetime.datetime.time()
            self.obj.type = 7
            self.obj.status = False
            self.obj.save()
            self.dobj.value = '{},{}.zip'.format(str(self.dobj.value), self.obj.verion)
            self.dobj.save()
        except Exception as e:
            logger.error("更新数据报错{}".format(e))

    def report(self):
        result = []
        goldData = []
        uiData = []
        try:
            uidiseases = auto_uirecord.objects.filter(autoid=self.obj.uid).values('caseid').annotate(
                success=Count(Case(When(result='匹配成功', then=0))), fail=Count(Case(When(result='匹配失败', then=0))),
                count=Count('caseid'))

            for i in uidiseases:
                error = int(i["count"]) - int(i["success"]) - int(i["fail"])
                disease = {
                    "diseases": i["diseases"],
                    "success": i["success"],
                    "fail": i["fail"],
                    "error": error
                }
                uiData.append(disease)

            smokediseases = smoke_record.objects.filter(smokeid=self.obj.smokeid).values('diseases').annotate(
                success=Count(Case(When(result='匹配成功', then=0))), fail=Count(Case(When(result='匹配失败', then=0))),
                count=Count('diseases'))

            for j in smokediseases:
                error = int(j["count"]) - int(j["success"]) - int(j["fail"])
                disease = {
                    "diseases": j["diseases"],
                    "success": j["success"],
                    "fail": j["fail"],
                    "error": error
                }
                goldData.append(disease)

            for k in ['成功', '失败']:
                smobj = smoke_record.objects.filter(smokeid=self.obj.smokeid, result__contains=k)
                uiobj = auto_uirecord.objects.filter(autoid=self.obj.uid, result__contains=k)
                result.append(smobj.count())
                result.append(uiobj.count())
            smerror = int(smoke_record.objects.filter(smokeid=self.obj.smokeid).count()) - int(result[0]) - int(
                result[2])
            uierror = int(auto_uirecord.objects.filter(autoid=self.obj.uid).count()) - int(result[1]) - int(
                result[3])
            data = {
                "basedata": [{
                    "version": self.obj.version,
                    "product": '金标准测试',
                    "success": result[0],
                    "fail": result[2],
                    "error": smerror
                }, {
                    "version": self.obj.version,
                    "product": 'UI自动化',
                    "success": result[1],
                    "fail": result[3],
                    "error": uierror
                }],
                "gold": {
                    "version": self.obj.version,
                    "product": '金标准测试',
                    "success": result[0],
                    "fail": result[2],
                    "error": smerror
                },
                "ui": {
                    "version": self.obj.version,
                    "product": 'UI自动化',
                    "success": result[1],
                    "fail": result[3],
                    "error": uierror
                },
                "goldrows": [
                    {'状态': '匹配成功', '数量': result[0]},
                    {'状态': '匹配失败', '数量': result[2]},
                    {'状态': '报错', '数量': smerror}
                ],
                "uirows": [
                    {'状态': '匹配成功', '数量': result[1]},
                    {'状态': '匹配失败', '数量': result[3]},
                    {'状态': '报错', '数量': uierror}
                ],
                "uiData": uiData,
                "goldData": goldData
            }
        except Exception as e:
            logger.error("数据报错{}".format(e))
        return data

    def setFlag(self, parm):  # 外部停止线程的操作函数
        self.Flag = parm  # boolean

    def setParm(self, parm):  # 外部修改内部信息函数
        self.Parm = parm

    def getParm(self):  # 外部获得内部信息函数
        return self.parm
