from .transport import SSHConnection
import threading
from django.conf import settings
from django.db.models import Count, When, Case
from ..models import install, dictionary, Server
from AutoInterface.models import gold_test, gold_record
from AutoDicom.models import duration
from AutoDicom.common.durarion import DurationThread
from AutoInterface.common.gold import GoldThread
from AutoUI.models import autoui, auto_uirecord
from ..common.biomind import RestartThread
import time
import datetime
import logging
from ..utils.keycloak.keycloakadmin import KeycloakAdm

logger = logging.getLogger(__name__)  # 这里使用 __name__ 动态搜索定义的 logger 配置


class InGoldThread(threading.Thread):
    def __init__(self, **kwargs):
        threading.Thread.__init__(self)
        self.Flag = True  # 停止标志位
        # self.count = kwargs["count"]  # 可用来被外部访问的
        # 性能测试id
        self.version = kwargs["version"]
        self.server = Server.objects.get(id='13')
        self.ssh = SSHConnection(host=self.server.host, pwd=self.server.pwd)
        
    def run(self):
        try:
            self.starttime = datetime.datetime.now()
            try:
                self.ssh.cmd(
                    "rm -rf cache.zip;")
                logger.info("Nightly Build Version:{}：更新 cache 文件".format(self.version))
                self.ssh.upload("/files1/classifier/orthanc.json",
                                "/home/biomind/.biomind/var/biomind/orthanc/orthanc.json")
                self.ssh.upload("/files1/classifier/cache.zip",
                                "/home/biomind/cache.zip")
                logger.info("Nightly Build Version:{}：解压cache文件".format(self.version))
                self.ssh.cmd(
                    "unzip -o cache.zip -d /home/biomind/.biomind/var/biomind/;")

            except Exception as e:
                logger.error("Nightly Build Version:{0}：更新json文件失败----失败原因：{1}".format(self.version, e))

            logger.info("Nightly Build Version:{}：重启服务".format(self.version))
            restart = RestartThread(id=self.server.id)
            restart.setDaemon(True)
            # 开始线程
            restart.start()

            logger.info("Nightly Build Version:{}：sheep 300 秒".format(self.version))
            time.sleep(300)
            self.createUser()
            logger.info("Nightly Build Version:{}：createUser".format(self.version))
            self.goldsmoke()
            self.duration()
            restart.setFlag = False
            self.ssh.close()
        except Exception as e:
            logger.error("Nightly Build Version:{0}：安装{1}版本失败----失败原因：{2}".format(self.version, self.obj.version, e))

    def createUser(self):
        try:
            logger.info("Nightly Build Version:{}：创建 3d 用户".format(self.version))
            user_info = {"username": "biomind3d", "enabled": True,
                         "credentials": [{"value": "engine3D.", "type": "password", }]}
            kc_adm = KeycloakAdm(orthanc_ip='{0}://{1}'.format(self.server.protocol, self.server.host))
            # kc_adm.update_user_add_group(user_info, 'admins')
            kc_adm.create_update_user_add_all_group(user_info)
        except Exception as e:
            logging.error('Failed to create User: %s!', e)

    def goldsmoke(self):
        try:
            data = {"version": self.version,
                    "diseases": "19,44,31,32,21,33,23,24,20,30,22,25,26",
                    "status": True,
                    "Host_id": 13,
                    "thread": 3,
                    "count": 127
                    }
            logger.info("Nightly Build Version:{}：创建金标准测试".format(self.version))
            smokeobj = gold_test.objects.create(**data)

            logger.info("Nightly Build Version:{}：执行金标准测试".format(self.version))
            testThread = GoldThread(smokeobj.id)
            # 设为保护线程，主进程结束会关闭线程
            testThread.setDaemon(True)
            # 开始线程
            testThread.start()
        except Exception as e:
            logger.error("Nightly Build Version:{0}：执行金标准测试报错{1}".format(self.version, e))

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
            logger.info("Nightly Build Version:{}：创建UI测试".format(self.version))
            uobj = autoui.objects.create(**data)
            self.obj.type = 6
            self.obj.uid = uobj.id
            self.obj.save()
            # testThread = GoldThread(smokeobj.id)
            # # 设为保护线程，主进程结束会关闭线程
            # testThread.setDaemon(True)
            # # 开始线程
            # testThread.start()
        except Exception as e:
            logger.error("Nightly Build Version:{0}：执行UI自动化报错{1}".format(self.version, e))

    def duration(self):
        try:
            data = {"server": self.server.host,
                    "port": 4242,
                    "aet": self.server.remarks,
                    "patientid": 'DT',
                    "patientname": 'Dt',
                    "dicom": "1,2,3,4,5,6,7,8,9,10,11,13,14,35,45",
                    "sendcount": 258,
                    "sleepcount": 100,
                    "sleeptime": 10,
                    "series": False,
                    "sendstatus": True,
                    "status": True,
                    "Host_id": 13,
                    "type": "Nightly",
                    "version": self.version
                    }
            logger.info("Nightly Build Version:{}：创建持续化测试".format(self.version))
            duobj = duration.objects.create(**data)

            logger.info("Nightly Build Version:{}：执行金标准测试".format(self.version))
            testThread = DurationThread(id=duobj.id)
            # 设为保护线程，主进程结束会关闭线程
            testThread.setDaemon(True)
            # 开始线程
            testThread.start()
        except Exception as e:
            logger.error("Nightly Build Version:{0}：执行金标准测试报错{1}".format(self.version, e))

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

            smokediseases = gold_record.objects.filter(smokeid=self.obj.smokeid).values('diseases').annotate(
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
                smobj = gold_record.objects.filter(smokeid=self.obj.smokeid, result__contains=k)
                uiobj = auto_uirecord.objects.filter(auto__autoid=self.obj.uid, result__contains=k)
                result.append(smobj.count())
                result.append(uiobj.count())
            smerror = int(gold_record.objects.filter(smokeid=self.obj.smokeid).count()) - int(result[0]) - int(
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
