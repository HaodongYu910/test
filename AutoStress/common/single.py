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
from AutoProject.common.PostgreSQL import connect_postgres
from AutoProject.common.regexUtil import csv
from AutoProject.models import Server, dictionary, uploadfile
from AutoProject.utils.graphql.graphql import *
from AutoProject.utils.keycloak.login_kc import login_keycloak
from AutoProject.common.transport import SSHConnection

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
class SingleThread(threading.Thread):
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

    def run(self):
        self.obj.teststatus = "单一开始"
        self.obj.status = True
        self.obj.save()

        try:
            # 已有数据 循环预测
            for i in self.testdata.split(","):
                imagecount = []
                uids = ""
                count = 0
                # 肺炎模型单独 按层厚 分类处理
                if int(i) in [9, 12]:
                    self.lung(i)
                    continue
                dictobj = dictionary.objects.get(id=i)

                sql = 'SELECT dr.studyinstanceuid,d.imagecount,d.slicenumber FROM duration_record dr JOIN dicom d ON dr.studyolduid = d.studyinstanceuid WHERE dr.duration_id = \'0{0}\'AND d.predictor ={1}'.format(
                    str(self.stressid), i)
                cursor = connection.cursor()
                cursor.execute(sql)
                ret = cursor.fetchall()
                start_date = datetime.datetime.now()
                # 循环调用graphql 自动预测
                for k in ret:
                    # 影像张数集合
                    imagecount.append(k[1])
                    # 测试数据的uid
                    uids = uids + '\'' + str(k.studyinstanceuid) + '\','
                    if count == self.obj.single:
                        break
                    graphql_query = '{ ' \
                                    'ai_biomind(' \
                                    'block : false' \
                                    ' study_uid: "' + str(k[0]) + '"' \
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
                time.sleep(300 * int(self.obj.single))
                self.SaveResult(uids, start_date, imagecount, dictobj.value, None)

                ssh = SSHConnection(host=self.obj.server, pwd=self.obj.Host.pwd)
                ssh.command("nohup sshpass -p {} biomind restart > restart.log 2>&1 &".format(self.obj.Host.pwd))
                time.sleep(500)
            self.obj.teststatus = "测试完成"
            self.obj.save()
        except Exception as e:
            logger.error("性能测试启动失败：{0}".format(e))
            self.obj.teststatus = "测试报错！~"
            self.obj.save()

    def lung(self, modelID):
        for i in ["1.0", "1.25", "1.5", "5.0", "10.0"]:
            imagecount = []
            uids = ""
            count = 0
            dictobj = dictionary.objects.get(id=modelID)

            sql = 'SELECT dr.studyinstanceuid,d.imagecount,d.slicenumber FROM duration_record dr JOIN dicom d ON dr.studyolduid = d.studyinstanceuid WHERE dr.duration_id = \'0{0}\'AND d.predictor ={1} AND d.slicenumber =\'{2}\''.format(
                str(self.stressid), modelID, i)
            cursor = connection.cursor()
            cursor.execute(sql)
            ret = cursor.fetchall()
            start_date = datetime.datetime.now()
            # 循环调用graphql 自动预测
            for k in ret:
                # 影像张数集合
                imagecount.append(k[1])
                # 测试数据的uid
                uids = uids + '\'' + str(k.studyinstanceuid) + '\','
                if count == self.obj.single:
                    break
                graphql_query = '{ ' \
                                'ai_biomind(' \
                                'block : false' \
                                ' study_uid: "' + str(k[0]) + '"' \
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
            time.sleep(300 * int(self.obj.single))
            self.SaveResult(uids, start_date, imagecount, dictobj.value, i)

            ssh = SSHConnection(host=self.obj.server, pwd=self.obj.Host.pwd)
            ssh.command("nohup sshpass -p {} biomind restart > restart.log 2>&1 &".format(self.obj.Host.pwd))
            time.sleep(500)

    # 测试结果
    def SaveResult(self, uids, start_date, imagecount, modelname , slicenumber):
        try:
            end_date = datetime.datetime.now()

            for type in ['prediction', 'job']:
                obj = dictionary.objects.get(key=type, status=1, type='stresssql')
                result = connect_postgres(database="orthanc",
                                          host=self.obj.Host.id,
                                          sql=obj.value.format(uids[:-1], start_date,
                                                               end_date))
                dict = result.to_dict(orient='records')
                try:
                    dict[0]["avgimages"], dict[0]["maximages"], dict[0]["minimages"] = str(
                        '%.2f' % np.mean(imagecount)), str(
                        np.max(imagecount)), str(np.min(imagecount))
                except:
                    dict[0]["avgimages"], dict[0]["maximages"], dict[0]["minimages"] = None, None, None
                dict[0]["version"] = self.obj.version
                dict[0]["modelname"] = modelname
                dict[0]["type"] = type + 'dy'
                dict[0]["slicenumber"] = slicenumber

                stressserializer = stress_result_Deserializer(data=dict[0])
                with transaction.atomic():
                    stressserializer.is_valid()
                    stressserializer.save()
        except Exception as e:
            logger.error("数据写入失败{}".format(e))

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

    def setFlag(self, parm):  # 外部停止线程的操作函数
        self.Flag = parm  # boolean

    def setParm(self, parm):  # 外部修改内部信息函数
        self.Parm = parm

    def getParm(self):  # 外部获得内部信息函数
        return self.parm
