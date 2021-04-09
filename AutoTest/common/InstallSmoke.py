from .transport import SSHConnection
import threading
from django.conf import settings
from django.db.models import Count, When, Case
from ..models import install, smoke, dictionary, smoke_record
from ..common.gold import SmokeThread
from AutoUI.models import autoui, auto_uirecord
import time
import datetime
import logging
from ..utils.keycloak.keycloakadmin import KeycloakAdm

logger = logging.getLogger(__name__)  # 这里使用 __name__ 动态搜索定义的 logger 配置


class InSmokeThread(threading.Thread):
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

    def run(self):
        try:
            self.starttime = datetime.datetime.now()
            try:
                logger.info("Installation{}：更新 orthanc 文件".format(self.id))
                self.ssh.upload("/files1/classifier/orthanc.json",
                                "/home/biomind/.biomind/var/biomind/orthanc/orthanc.json")
                logger.info("Installation{}：更新classification_votes文件".format(self.id))
                self.ssh.upload("/files1/classifier/classification_votes.json",
                                "/home/biomind/.biomind/var/biomind/cache/series_classifier/classification_votes.json")

                logger.info("Installation{}：更新predefined_classifier文件".format(self.id))
                self.ssh.upload("/files1/classifier/predefined_classifier.json",
                                "/home/biomind/.biomind/var/biomind/cache/series_classifier/predefined_classifier.json")

                logger.info("Installation{}：更新special_classifier文件".format(self.id))
                self.ssh.upload("/files1/classifier/special_classifier.json",
                                "/home/biomind/.biomind/var/biomind/cache/series_classifier/special_classifier.json")

            except Exception as e:
                logger.error("Installation{0}：更新json文件失败----失败原因：{1}".format(self.id, e))
            self.restart()
            logger.info("Installation{}：sheep 200 秒".format(self.id))
            time.sleep(300)
            self.goldsmoke()
            self.finish()
        except Exception as e:
            self.obj.status = False
            self.obj.save()
            logger.error("Installation{0}：安装{1}版本失败----失败原因：{2}".format(self.id, self.obj.version, e))

    def restart(self):
        try:
            if self.Flag is True:
                logger.info("Installation{}：配置 configure".format(self.id))
                try:
                    self.ssh.configure(self.obj.server, str(self.obj.Host.protocol))
                    logger.info("Installation{}：重启服务".format(self.id))
                    self.ssh.cmd(
                        "nohup sshpass -p {} biomind start >> /home/biomind/restart.log 2>&1 &;".format(
                            self.pwd))
                except Exception as e:
                    logger.error("Installation{0}：重启服务失败----失败原因：{1}".format(self.id, e))
                self.ssh.close()
        except Exception as e:
            self.obj.status = False
            self.obj.save()
            logger.error("Installation{0}：重启服务失败{1}".format(self.id,e))

    def createUser(self):
        try:
            logger.info("Installation{}：创建 3d 用户".format(self.id))
            user_info = {"username": "biomind3d", "enabled": True,
                         "credentials": [{"value": "engine3D.", "type": "password", }]}
            kc_adm = KeycloakAdm(orthanc_ip='{0}://{1}'.format(self.obj.Host.protocol, self.obj.Host.host))
            # kc_adm.update_user_add_group(user_info, 'admins')
            kc_adm.create_update_user_add_all_group(user_info)
        except Exception as e:
            logging.error('Failed to create User: %s!', e)

    def goldsmoke(self):
        try:
            data = {"version": self.obj.version,
                    "diseases": "19,44,31,32,21,33,23,24,20,30,22,25,26",
                    "status": True,
                    "Host_id": int(self.obj.Host_id),
                    "thread": 3,
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

    def report(self):
        result = []
        goldData = []
        uiData = []
        try:
            uidiseases = auto_uirecord.objects.filter(auto__autoid=self.obj.uid).values('case_id').annotate(

                success=Count(Case(When(result='匹配成功', then=0))), fail=Count(Case(When(result='匹配失败', then=0))),
                count=Count('case_id'))

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
                uiobj = auto_uirecord.objects.filter(auto__autoid=self.obj.uid, result__contains=k)
                result.append(smobj.count())
                result.append(uiobj.count())
            smerror = int(smoke_record.objects.filter(smokeid=self.obj.smokeid).count()) - int(result[0]) - int(
                result[2])
            uierror = int(auto_uirecord.objects.filter(auto__autoid=self.obj.uid).count()) - int(result[1]) - int(
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
            return {}
        return data

    def setFlag(self, parm):  # 外部停止线程的操作函数
        self.Flag = parm  # boolean

    def setParm(self, parm):  # 外部修改内部信息函数
        self.Parm = parm

    def getParm(self):  # 外部获得内部信息函数
        return self.parm