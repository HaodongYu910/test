from .transport import SSHConnection
import threading
from django.conf import settings
from django.db.models import Count, When, Case
from ..models import install, smoke, dictionary, smoke_record
import os
from ..common.gold import SmokeThread
from AutoUI.models import autoui, auto_uirecord
import time, datetime
import logging

logger = logging.getLogger(__name__)  # 这里使用 __name__ 动态搜索定义的 logger 配置

def deldata(server, Iid, passwd):
    try:
        ssh = SSHConnection(host=server, pwd=passwd)
        ssh.cmd("sshpass -p {} biomind stop".format(passwd))
        logger.info("Installation{}：停止旧服务".format(Iid))
        ssh.shcmd("sshpass -p y docker system prune")
        logger.info("Installation{}：docker system prune".format(Iid))
        ssh.cmd("docker volume rm $(docker volume ls -q)")
        logger.info("Installation{}：docker volume rm $(docker volume ls -q)".format(Iid))
        ssh.cmd("sshpass -p {} sudo rm -rf /lfs/biomind".format(passwd))
        logger.info("Installation{}：删除/lfs/biomind".format(Iid))
        ssh.cmd("sshpass -p {} sudo rm -rf /lfs/Biomind-3Dserver".format(passwd))
        logger.info("Installation{}：删除 Biomind-3Dserver".format(Iid))
        ssh.cmd("sshpass -p {} sudo rm -rf /home/biomind/.biomind".format(passwd))
        logger.info("Installation{}：删除 .biomind".format(Iid))
        ssh.cmd("sshpass -p {} sudo rm -rf /home/biomind/.3D-biomind".format(passwd))
        logger.info("Installation{}：删除 .3D-biomind".format(Iid))
        ssh.cmd("sshpass -p {} sudo rpm -e supervisor".format(passwd))
        logger.info("Installation{}：删除 supervisor".format(Iid))
        ssh.cmd("sshpass -p {} sudo rm -rf /etc/yum.repos.d/3dlocal.repo".format(passwd))
        logger.info("Installation{}：删除完成".format(Iid))
    except Exception as e:
        logger.error("Installation{0}：全新安装失败：{1}".format(Iid,e))


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
        self.dobj = dictionary.objects.get(type='install', key='oldversion')
        self.oldversion = self.dobj.value.split(',')

    def downFile(self, version):
        try:
            downssh = SSHConnection(host='192.168.2.111', pwd='P@ssw0rd2111')
            if version:
                downpath = '/lfs/nextcloud/data/mengyue.he@biomind.ai/files/Version_for_QA/{0}.zip'.format(version)
                path = '/files/History_version/{0}'.format(version)
                if not os.path.exists(path):
                    os.makedirs(path)
                    logger.info("Installation{0}：创建备份文件夹{1}".format(self.id, version))
                logger.info("Installation{0}：下载备份最新安装包{1}.zip".format(self.id, version))
                downssh.download(self.localpath, downpath)
                downssh.close()
            else:
                filelist = downssh.cmd("ls /lfs/nextcloud/data/mengyue.he@biomind.ai/files/Version_for_QA/")
                for i in str(filelist, encoding="utf-8").split('\n'):
                    if i not in self.oldversion and i:
                        version = i
                downpath = '/lfs/nextcloud/data/mengyue.he@biomind.ai/files/Version_for_QA/{}'.format(version)
                path = '/files/History_version/{}/'.format(version[:-4])
                self.localpath = '/files/History_version/{0}/{1}'.format(version[:-4], version)
                if not os.path.exists(path):
                    os.makedirs(path)
                    logger.info("Installation{0}：创建备份文件夹{1}".format(self.id, version[:-4]))
                logger.info("Installation{0}：下载备份最新安装包{1}.zip".format(self.id, version[:-4]))
                downssh.download(self.localpath, downpath)
                downssh.close()
                self.obj.version = version[:-4]
                self.obj.save()
        except Exception as e:
            self.obj.status = False
            self.obj.save()
            logger.error("Installation{0}：下载最新版本报错{}".format(self.id, e))

    def run(self):
        try:
            self.obj.starttime = datetime.datetime.now()
            self.obj.status = True
            self.obj.type = 1
            self.obj.save()
            if self.obj.installstatus is True:
                deldata(self.obj.server, self.id, self.pwd)
            if self.obj.version:
                self.localpath = '/files/History_version/{0}/{1}.zip'.format(self.obj.version, self.obj.version)
                if not os.path.exists(self.localpath):
                    self.obj.type = 2
                    self.obj.save()
                    self.downFile(version=self.obj.version)
            else:
                self.obj.type = 2
                self.obj.save()
                self.downFile(version='')
            self.obj.type = 3
            self.obj.save()
            if not os.path.exists("/home/biomind/{}".format(self.obj.version)):
                logger.info("Installation{0}：上传最新安装包{1}.zip".format(self.id,self.obj.version))
                self.ssh.upload(self.localpath, "/home/biomind/QaInstall.zip")
                self.ssh.cmd("sshpass -p {0} sudo rm -rf {1}/".format(self.pwd,self.obj.version))
                logger.info("Installation{0}：解压安装包 QaInstall.zip".format(self.id))
                self.ssh.cmd("unzip {}".format("QaInstall.zip"))
            logger.info("Installation{}：停止服务".format(self.id))
            self.ssh.cmd("sshpass -p {} biomind stop;".format(self.pwd))
            logger.info("Installation{}：安装最新版本".format(self.id))
            self.ssh.cmd("cd {0};sshpass -p {1} bash setup_engine.sh;".format(self.obj.version, self.pwd))
            time.sleep(5)
            try:
                logger.info("Installation{}：更新orthanc文件".format(self.id))
                self.ssh.upload("/files1/classifier/orthanc.json".format(settings.BASE_DIR),
                                "/home/biomind/.biomind/var/biomind/orthanc/orthanc.json")

                logger.info("Installation{}：更新classification_votes文件".format(self.id))
                self.ssh.upload("/files1/classifier/classification_votes.json".format(settings.BASE_DIR),
                                "/home/biomind/.biomind/var/biomind/cache/series_classifier/classification_votes.json")

                logger.info("Installation{}：更新predefined_classifier文件".format(self.id))
                self.ssh.upload("/files1/classifier/predefined_classifier.json".format(settings.BASE_DIR),
                                "/home/biomind/.biomind/var/biomind/cache/series_classifier/predefined_classifier.json")

                logger.info("Installation{}：更新special_classifier文件".format(self.id))
                self.ssh.upload("/files1/classifier/special_classifier.json".format(settings.BASE_DIR),
                                "/home/biomind/.biomind/var/biomind/cache/series_classifier/special_classifier.json")
            except Exception as e:
                logger.error("Installation{0}：更新json文件失败----失败原因：{1}".format(self.id, e))
            self.restart()
            self.goldsmoke()
        except Exception as e:
            self.obj.status = False
            self.obj.save()
            logger.error("Installation{0}：安装{1}版本失败----失败原因：{2}".format(self.id, self.obj.version, e))

    def restart(self):
        try:
            logger.info("Installation{}：配置 configure".format(self.id))
            self.ssh.configure(self.obj.server, str(self.obj.Host.protocol))
            self.obj.type = 4
            self.obj.save()
            logger.info("Installation{}：重启服务".format(self.id))
            self.ssh.cmd("sshpass -p {} biomind start prod master;".format(self.pwd))
            self.ssh.close()
            time.sleep(200)
            # try:
            #     groups = KeycloakAdmin.get_groups()
            #     KeycloakAdmin.create_user(
            #     'test', 'Asd@123456', [
            #         x['id'] for x in groups])  # 获得角色(分组)ID

            # except Exception as e:
            #     logging.error('Failed to create User: %s!', e)
        except Exception as e:
            self.obj.status = False
            self.obj.save()
            logger.error("Installation{0}：重启服务失败{1}".format(self.id,e))

    def goldsmoke(self):
        try:
            data = {"version": self.obj.version,
                    "diseases": "19,44,31,32,21,33,23,24,20,30,22,25,26",
                    "status": True,
                    "hostid": self.obj.Host_id,
                    "thread": 1,
                    "count": 127
                    }
            logger.info("Installation{}：创建金标准测试".format(self.id))
            smokeobj = smoke.objects.create(**data)
            self.obj.status = False
            self.obj.type = 5
            self.obj.smokeid = smokeobj.id
            self.obj.save()
            logger.info("Installation{}：执行金标准测试".format(self.id))
            testThread = SmokeThread(smokeobj.id)
            # 设为保护线程，主进程结束会关闭线程
            testThread.setDaemon(True)
            # 开始线程
            testThread.start()
        except Exception as e:
            self.obj.status = False
            self.obj.save()
            logger.error("Installation{0}：执行金标准测试报错{1}".format(self.id, e))

    def UiTest(self):

        try:
            data = {"version": self.obj.version,
                    "setup": "1",
                    "cases": "1",
                    "tearDown": "1",
                    "status": True,
                    "hostid": self.obj.hostid,
                    "thread": 1
                    }
            logger.info("Installation{}：创建UI测试".format(self.id))
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
            logger.error("Installation{0}：执行UI自动化报错{1}".format(self.id, e))

    def finish(self):
        try:

            self.obj.starttime = datetime.datetime.time()
            self.obj.type = 7
            self.obj.status = False
            self.obj.save()
            self.dobj.value = '{},{}.zip'.format(str(self.dobj.value), self.obj.verion)
            self.dobj.save()
            logger.info("Installation{0}：部署完成".format(self.id))
        except Exception as e:
            logger.error("Installation{0}：更新数据报错{1}".format(self.id, e))

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
