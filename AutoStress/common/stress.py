import datetime
import os
import shutil
import threading
import time

import numpy as np
from django.db import connection
from django.db import transaction
from django.conf import settings
from ..models import stress_record, stress_result, stress
from ..serializers import stress_result_Deserializer
from .loganalys import errorLogger
from AutoTest.common.PostgreSQL import connect_postgres
from AutoTest.common.regexUtil import csv
from AutoTest.models import Server, dictionary, uploadfile
from AutoTest.utils.graphql.graphql import *
from AutoTest.utils.keycloak.login_kc import login_keycloak
from AutoTest.common.transport import SSHConnection

from AutoDicom.common.dicomBase import checkuid, voteData
from AutoDicom.models import duration_record, dicom
from django.conf import settings

logger = logging.getLogger(__name__)


# 删除dicom报告
def delreport(kc, studyinstanceuid):
    try:
        graphql_query = 'mutation{ ' \
                        'deleteReport( studyuid:' + str(studyinstanceuid) + ' )' \
                                                                            'deleteProtocol( studyuid:' + str(
            studyinstanceuid) + ' ) }'
        graphql_Interface(graphql_query, kc)
    except:
        logger.error("删除失败{0}".format(studyinstanceuid))


# 保存数据
def saveData(**kwargs):
    try:
        if kwargs["type"] in ["predictionJZ", "lung_prediction"]:
            sql = dictionary.objects.get(key="predictionJZ", type="sql", status=True)
            result = connect_postgres(database="orthanc", host=kwargs["id"],
                                      sql=sql.value.format(kwargs["studyuid"], kwargs["startdate"]))
            kwargs["datatest"]["type"] = kwargs["type"]
            try:
                kwargs["datatest"]["avg"] = str(result.to_dict(orient='records')[0]["avg"])
            except:
                kwargs["datatest"]["avg"] = 0
            try:
                kwargs["datatest"]["median"] = str(result.to_dict(orient='records')[0]["median"])
            except:
                kwargs["datatest"]["avg"] = 0
            try:
                kwargs["datatest"]["min"] = str(result.to_dict(orient='records')[0]["min"])
            except:
                kwargs["datatest"]["avg"] = 0
            try:
                kwargs["datatest"]["max"] = str(result.to_dict(orient='records')[0]["max"])
            except:
                kwargs["datatest"]["avg"] = 0
        else:
            kwargs["datatest"]["type"] = kwargs["type"]

        _result = stress_result_Deserializer(data=kwargs["datatest"])
        with transaction.atomic():
            _result.is_valid()
            _result.save()
    except Exception as e:
        logger.error("保存预测基准测试数据失败：{0}".format(e))


# 生成自动预测测试数据
def stresscache(stressid):
    obj = stress.objects.get(stressid=stressid)
    # 循环病种存储 测试数据
    for i in obj.testdata.split(","):
        dictobj = dictionary.objects.get(id=i)
        # 查询预测成功的数据 作为压测数据
        # sql = 'select  DISTINCT studyuid from  prediction_metrics where modelname =\'brainctp\' ORDER BY modelname';
        sql = 'select  DISTINCT studyuid from  prediction_metrics where modelname like \'%{0}%\''.format(dictobj.key)
        results = connect_postgres(database="orthanc", host=obj.Host_id, sql=sql).to_dict(orient='records')
        # 循环插入数据
        for j in results:
            logger.info(j['studyuid'])
            # graphql_query, imagecount, slicenumber=None,None,None
            graphql_query, imagecount, slicenumber = voteData(j['studyuid'], obj.loadserver, int(i))
            data = {"stressid": stressid,
                    "studyuid": j['studyuid'],
                    "imagecount": imagecount,
                    "slicenumber": slicenumber,
                    "diseases": i,
                    "graphql": None
                    }
            stress_record.objects.create(**data)


def savecsv(path, graphql_query):
    f = open('{0}'.format(path), 'a', encoding='utf-8', newline="")
    csv_writer = csv.writer(f)
    csv_writer.writerow(graphql_query)
    f.close()


def saveStressddt(stressid, path):
    imagelist = []
    ii = 0
    # 查询测试配置
    obj = stress.objects.get(stressid=stressid)
    savecsv('{}/data/config.csv'.format(path),
            [obj.loadserver, 'biomind3d', 'engine3D.', obj.thread, obj.synchroniz, obj.ramp, time, obj.version,
             obj.loop_count])
    # 影像id
    image = connect_postgres(database="orthanc", host=obj.Host_id,
                             sql='select publicid from image ORDER BY internalid desc LIMIT 100')
    imagedata = image.to_dict(orient='records')
    for j in imagedata:
        imagelist.append(j["publicid"])
    # 循环生成压测数据
    for i in obj.testdata.split(","):
        if int(i) in [4, 7, 8, 10]:
            obd = dictionary.objects.get(id=i)
            sqlobj = dictionary.objects.get(type='sql', key='3d')
            sql = sqlobj.value.format(obd.key, obj.thread)
            stressdict = connect_postgres(database="orthanc", host=obj.Host_id,
                                          sql=sql)
            stressdata = stressdict.to_dict(orient='records')
            try:
                for k in stressdata:
                    savecsv('{}/data/data.csv'.format(path, str(i)),
                            [k["publicid"], k["studyinstanceuid"], k["publicid"], k['modality'], obd.remarks,
                             imagelist[ii]])
                    ii = ii + 1
            except Exception as e:
                continue


# 性能测试
class StressThread(threading.Thread):
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
        self.single = 20

    #  基准测试
    def Manual(self):
        self.obj.status = True
        self.obj.save()
        count = int(self.obj.ramp)
        try:
            for i in self.obj.testdata.split(","):
                stressdata = dicom.objects.filter(predictor=i.strip(), stressstatus=2)
                for k in stressdata:
                    avglist = []
                    checkuid(self.obj.Host_id, self.server, str(k.id))
                    delreport(self.kc, str(k.studyinstanceuid))
                    # 循环 测试基准数据
                    startdate = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                    for j in range(count):
                        try:
                            if self.Flag is False:
                                break
                            # 开始时间
                            starttime = time.time()
                            result = graphql_Interface(k.graphql, self.kc)
                            ai_biomind = result['ai_biomind']
                            avgtime = time.time() - starttime
                            avglist.append(avgtime)
                            time.sleep(10)
                        except Exception as e:
                            logger.error("执行预测失败：{0}".format(k.studyinstanceuid))
                            continue

                    jobtype = 'jobJZ'
                    predictiontype = 'predictionJZ'
                    avgtime = str('%.2f' % np.mean(avglist))

                    datatest = {
                        "Stress": self.stressid,
                        "version": self.obj.version,
                        "count": count,
                        "modelname": k.predictor,
                        "slicenumber": k.slicenumber,
                        "avg": avgtime,
                        "min": str('%.2f' % min(avglist)),
                        "max": str('%.2f' % max(avglist)),
                        "minimages": k.imagecount,
                        "maximages": k.imagecount,
                        "avgimages": k.imagecount
                    }
                    saveData(datatest=datatest,
                             type=jobtype
                             )
                    saveData(datatest=datatest,
                             type=predictiontype,
                             id=self.obj.Host_id,
                             studyuid=k.studyinstanceuid,
                             startdate=startdate
                             )
            self.obj.status = False
            self.obj.save()
        except Exception as e:
            logger.error("执行预测基准测试数据失败：{0}".format(e))

    def Single(self):
        starttime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        endtime = (datetime.datetime.now() + datetime.timedelta(hours=1)).strftime("%Y-%m-%d %H:%M:%S")
        self.obj.save()
        try:
            # 已有数据 循环预测
            for i in self.testdata.split(","):
                count = 0
                dicobj = dictionary.objects.get(id=i)
                durobj = duration_record.objects.filter(model=dicobj.value, duration_id=self.obj.id,
                                                        aistatus__in=[2, 3])
                # 循环调用graphql 自动预测
                for k in durobj:
                    if count == self.single:
                        break
                    graphql_query = '{ ' \
                                    'ai_biomind(' \
                                    'block : false' \
                                    ' study_uid: "' + str(k.studyinstanceuid) + '"' \
                                                                                ' protocols: {' \
                                                                                ' penable_cached_results: false' \
                                                                                ' }' \
                                                                                '){' \
                                                                                '  pprediction' \
                                                                                '  preport' \
                                                                                '  pcontour' \
                                                                                '  pmodels' \
                                                                                '  pstudy_uid' \
                                                                                '}' \
                                                                                '}'
                    graphql_Interface(graphql_query, self.kc)
                time.sleep(180*int(self.single))
                ssh = SSHConnection(host=self.obj.server, pwd=self.obj.Host.pwd)
                ssh.cmd(
                    "nohup sshpass -p {} biomind start >> /home/biomind/restart.log 2>&1 &;".format(self.obj.Host.pwd))
                time.sleep(300)
        except Exception as e:
            logger.error("性能测试启动失败：{0}".format(e))

    # 混合预测压测循环
    def AutoPrediction(self, type):
        self.obj.start_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.obj.save()
        try:
            # 已有数据 循环预测
            if type != "send":
                # 查询测试数据
                for i in self.obj.testdata.split(","):
                    stressdata = dicom.objects.filter(predictor=i.strip())
                    for j in stressdata:
                        checkuid(self.obj.Host_id, self.server, j.id)
                        delreport(self.kc, j.studyuid)
                    # 循环调用graphql 自动预测
                    for k in stressdata:
                        graphql_query = '{ ' \
                                        'ai_biomind(' \
                                        'block : false' \
                                        ' study_uid: "' + str(k.studyuid) + '"' \
                                                                            ' protocols: {' \
                                                                            ' penable_cached_results: false' \
                                                                            ' }' \
                                                                            '){' \
                                                                            '  pprediction' \
                                                                            '  preport' \
                                                                            '  pcontour' \
                                                                            '  pmodels' \
                                                                            '  pstudy_uid' \
                                                                            '}' \
                                                                            '}'

                        graphql_Interface(graphql_query, self.kc)
                        time.sleep(1)
            # 发送dicom数据 预测
            else:
                for i in self.obj.testdata.split(","):
                    cmd = ('nohup /home/biomind/.local/share/virtualenvs/biomind-dvb8lGiB/bin/python3'
                           ' /home/biomind/Biomind_Test_Platform/AutoDicom/common/dicomSend.py '
                           '--ip {0} --aet {1} '
                           '--port {2} '
                           '--patientid {3} '
                           '--patientname {4} '
                           '--folderid {5} '
                           '--durationid {6} '
                           '--end {7} '
                           '--sleepcount {8} '
                           '--sleeptime {9} '
                           '--series {10} &').format(self.server, self.obj.Host.remarks, self.obj.Host.port,
                                                     "ST{}".format(str(i).strip()), "st{}".format(str(i).strip()),
                                                     str(i).strip(), '0{}'.format(self.stressid),
                                                     int(self.obj.loop_count), 8787, 0, 0)
                    os.system(cmd)
                    logger.info(cmd)
            self.obj.status = True
            self.obj.save()
            return True
        except Exception as e:
            return False
            logger.error("性能测试启动失败：{0}".format(e))

    # 执行 jmeter 脚本
    def jmeterStress(self):
        jmeterobj = uploadfile.objects.filter(fileid=self.stressid)
        path = settings.LOG_PATH
        if not os.path.exists('{}/data'.format(path)):
            os.mkdir('{}/data'.format(path))
        else:
            shutil.rmtree('{}/data'.format(path))
            os.mkdir('{}/data'.format(path))
        saveStressddt(self.stressid, path)
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

    # 测试结果
    def SaveResult(self):
        # 模型预测时间 job时间
        for type in ['prediction', 'job']:
            obj = dictionary.objects.get(key=type, status=1, type='stresssql')
            # 测试模型数据查询
            for i in self.testdata.split(","):
                infos = {}
                sql = 'SELECT dr.studyinstanceuid ,d.imagecount,d.slicenumber FROM duration_record dr JOIN dicom d ON dr.studyolduid = d.studyinstanceuid WHERE dr.duration_id = \'0{0}\'AND d.predictor ={1}'.format(
                    str(self.stressid), i)
                cursor = connection.cursor()
                cursor.execute(sql)
                ret = cursor.fetchall()
                # 生成查询数据
                for j in ret:
                    if infos.__contains__(j[2]) is False:
                        infos = {
                            j[2]: {"uids": '\'' + str(j[0]) + '\',',
                                   "image": [j[1]]
                                   }
                        }
                    else:
                        infos[j[2]]["uids"] = infos[j[2]]["uids"] + '\'' + str(j[0]) + '\','
                        infos[j[2]]["image"].append(j[1])
                try:
                    # 循环查询结果
                    for k, v in infos.items():
                        result = connect_postgres(database="orthanc",
                                                  host=self.obj.Host.id,
                                                  sql=obj.value.format(v["uids"][:-1], self.obj.start_date,
                                                                       self.obj.end_date))
                        dict = result.to_dict(orient='records')
                        try:
                            dict[0]["avgimages"], dict[0]["maximages"], dict[0]["minimages"] = str(
                                '%.2f' % np.mean(v["image"])), str(
                                np.max(v["image"])), str(np.min(v["image"]))
                        except:
                            dict[0]["avgimages"], dict[0]["maximages"], dict[0]["minimages"] = None, None, None
                        dict[0]["version"] = self.obj.version
                        dict[0]["modelname"] = i
                        dict[0]["type"] = type
                        dict[0]["slicenumber"] = k

                        stressserializer = stress_result_Deserializer(data=dict[0])
                        with transaction.atomic():
                            stressserializer.is_valid()
                            stressserializer.save()
                except Exception as e:
                    logger.error("数据写入失败{}".format(e))
                    continue

    # 保存 job 结果数据
    def SaveRecord(self):
        # 查询测试时间 job 数据
        for j in ["predictionrecord", "jobmetrics"]:
            sqlobj = dictionary.objects.get(key=j)
            sql = sqlobj.value.format(self.obj.start_date, self.obj.end_date)
            result = connect_postgres(database="orthanc", host=self.obj.Host.id,
                                      sql=sql)
            dict = result.to_dict(orient='records')
            # 循环数据保存
            for i in dict:
                try:
                    drobj = duration_record.objects.get(studyinstanceuid=i["studyuid"])
                    dicomobj = dicom.objects.get(studyinstanceuid=drobj.studyolduid)
                    data = {
                        "studyuid": i["studyuid"],
                        "job_id": self.server,
                        "start": str(i["start"])[:19],
                        "end": str(i["end"])[:19],
                        "sec": str(i["sec"]),
                        "modelname": dicomobj.predictor,
                        "version": self.obj.version,
                        "type": 'job',
                        "Stress_id": self.stressid,
                        "images": dicomobj.imagecount,
                        "slicenumber": dicomobj.slicenumber,
                        "type": j
                    }
                    stress_record.objects.create(**data)
                except Exception as e:
                    continue

    def errorlog(self):
        ssh = SSHConnection(host=self.server, port=22, user=self.obj.Host.user, pwd=self.obj.Host.pwd)
        os.system("rm -rf {}/pm2.zip".format(settings.LOG_PATH))
        downpath = '/home/biomind/.biomind/lib/versions/{}/logs/pm2'.format(self.obj.version)
        ospath = '{}/pm2.zip'.format(settings.LOG_PATH)
        ssh.download(ospath, downpath)
        errorLogger(self.stressid, self.obj.version, ospath)
        ssh.close()

    def setFlag(self, parm):  # 外部停止线程的操作函数
        self.Flag = parm  # boolean

    def setParm(self, parm):  # 外部修改内部信息函数
        self.Parm = parm

    def getParm(self):  # 外部获得内部信息函数
        return self.parm