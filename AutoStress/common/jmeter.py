import datetime
import os
import shutil
import threading
import time

from ..models import  stress

from AutoProject.common.PostgreSQL import connect_postgres
from AutoProject.common.regexUtil import csv
from AutoProject.models import  dictionary, uploadfile
from AutoProject.utils.graphql.graphql import *
from AutoProject.utils.keycloak.login_kc import login_keycloak

from django.conf import settings

logger = logging.getLogger(__name__)


def savecsv(path, query):
    f = open('{0}'.format(path), 'a', encoding='utf-8', newline="")
    csv_writer = csv.writer(f)
    csv_writer.writerow(query)
    f.close()

# Jmeter 性能测试
class JmeterThread(threading.Thread):
    def __init__(self, *args, **kwargs):
        threading.Thread.__init__(self)
        self.Flag = True  # 停止标志位
        # self.count = kwargs["count"]  # 可用来被外部访问的
        # 性能测试id
        self.stressid = kwargs["stressid"]
        self.obj = stress.objects.get(stressid=self.stressid)
        self.server = self.obj.Host.host
        self.testdata = self.obj.testdata
        self.kc = login_keycloak(self.obj.Host_id)

    # 执行 jmeter 脚本
    def run(self):
        jmeterobj = uploadfile.objects.filter(fileid=self.stressid)
        path = settings.LOG_PATH
        if not os.path.exists('{0}/{1}'.format(path, self.server)):
            os.mkdir('{0}/{1}'.format(path, self.server))
        else:
            shutil.rmtree('{0}/{1}'.format(path, self.server))
            os.mkdir('{0}/{1}'.format(path, self.server))
        self.saveStressddt(path)
        # 执行jmeter
        try:
            for j in jmeterobj:
                start_time = datetime.datetime.now().strftime("%Y-%m-%d%H%M%S")
                cmd = 'nohup jmeter -n -t {0}/{1} -l /home/biomind/logs/{2}.jtl -j /home/biomind/logs/jmeter{3}.log &'.format(
                    j.fileurl, j.filename, start_time, start_time)
                logger.info(cmd)
                os.system(cmd)
        except Exception as e:
            logger.error("执行jmeter失败{0}".format(e))

    def saveStressddt(self, path):
        imagelist = []
        ii = 0
        # 查询测试配置

        savecsv('{0}/{1}/config.csv'.format(path, self.server),
                [self.obj.loadserver, 'biomind3d', 'engine3D.', self.obj.thread, self.obj.synchroniz, self.obj.ramp, time, self.obj.version,
                 self.obj.loop_count])
        # 影像id
        image = connect_postgres(database="orthanc", host=self.obj.Host_id,
                                 sql='select publicid from image ORDER BY internalid desc LIMIT 100')
        imagedata = image.to_dict(orient='records')
        for j in imagedata:
            imagelist.append(j["publicid"])
        # 循环生成压测数据
        for i in self.obj.testdata.split(","):
            if int(i) in [4, 7, 8, 10]:
                obd = dictionary.objects.get(id=i)
                sqlobj = dictionary.objects.get(type='sql', key='3d')
                sql = sqlobj.value.format(obd.key, self.obj.thread)
                stressdict = connect_postgres(database="orthanc", host=self.obj.Host_id,
                                              sql=sql)
                stressdata = stressdict.to_dict(orient='records')
                try:
                    for k in stressdata:
                        savecsv('{0}/{1}/data.csv'.format(path, str(self.server)),
                                [k["publicid"], k["studyinstanceuid"], k["publicid"], k['modality'], obd.value,
                                 imagelist[ii]])
                        ii = ii + 1
                except Exception as e:
                    continue

    def setFlag(self, parm):  # 外部停止线程的操作函数
        self.Flag = parm  # boolean

    def setParm(self, parm):  # 外部修改内部信息函数
        self.Parm = parm

    def getParm(self):  # 外部获得内部信息函数
        return self.parm
