from TestPlatform.models import dicom_record, dictionary, stress_record, stress_result, uploadfile, stress
from django.db import transaction
from TestPlatform.serializers import dicomrecord_Serializer
from ..dicom.dicomdetail import voteData
from ..stress.PerformanceResult import saveResult
from .PerformanceResult import lung
from ..dicom.dicomdetail import checkuid
from ...utils.keycloak.login_kc import *
from TestPlatform.utils.graphql.graphql import *
from TestPlatform.common.regexUtil import *
import os, time
import shutil
import numpy as np

logger = logging.getLogger(__name__)


# 修改数据
def update_data(data):
    obj = dicom_record.objects.get(testid=data["testid"])
    serializer = dicomrecord_Serializer(data=data)
    with transaction.atomic():
        if serializer.is_valid():
            serializer.update(instance=obj, validated_data=data)


# 调用graphql 存储记录接口
def graphql_prediction(data, kc):
    try:
        start_time = time.time()
        results = graphql_Interface(data, kc)
        data['duration'] = time.time() - start_time
        data['report'] = str(results['ai_biomind']['preport'])
        stress_detailserializer = dicomrecord_Serializer(data=data)
        with transaction.atomic():
            stress_detailserializer.is_valid()
            stress_detailserializer.save()
    except Exception as e:
        logger.error('Query failed: {0}'.format(e))
        return e
    return True


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
        if kwargs["type"] in ["predictionJZ","lung_prediction"]:
            sql=dictionary.objects.get(key="predictionJZ",type="sql",status=True)
            result = connect_to_postgres(kwargs["ip"],sql.value.format(kwargs["studyuid"],kwargs["count"]))
            datatest = kwargs["datatest"]
            datatest["type"] = kwargs["type"]
            datatest["avg"] = str(result.to_dict(orient='records')[0]["avg"])
            datatest["median"] =str( result.to_dict(orient='records')[0]["median"])
            datatest["min"] = str( result.to_dict(orient='records')[0]["min"])
            datatest["max"] = str( result.to_dict(orient='records')[0]["max"])
        else:
            datatest = kwargs["datatest"]
            datatest["type"]= kwargs["type"]
        stress_result.objects.create(**datatest)
    except Exception as e:
        logger.error("保存预测基准测试数据失败：{0}".format(e))

#  基准/单一手动预测
def Manual(serverID, serverIP, version,id,count,testdata):
    kc = login_keycloak(serverID)
    try:
        for i in testdata.split(","):
            stressdata = stress_record.objects.filter(diseases=i.strip(),benchmarkstatus=True)
            for k in stressdata:
                avglist = []
                checkuid(serverID, serverIP, str(k.stressid))
                obj = dictionary.objects.get(id=k.diseases)
                if str(k.diseases) in ["9","6","8"]:
                    manager = "\",\"artifacts_manager\"]])"
                else:
                    manager = "\"]])"
                graphql_query = "{ ai_biomind (" \
                                "study_uid:\"" + str(k.studyuid) + "\", protocols:" \
                                                                   "{ pothers: " \
                                                                   "{ disable_negative_voting:false} " \
                                                                   "penable_cached_results:false pconfig:{} " \
                                                                   "planguage:\"zh-cn\" " \
                                                                   " puser_id:\"biomind\" " \
                                                                   "pseries_classifier:" + str(k.graphql) + "}" \
                                                                                                            "routes: [[\"generate_series\",\"series_classifier\",\"" + str(
                    obj.value) + manager +" { pprediction pmetadata SOPInstanceUID pconfig  pseries_classifier pstatus_code } }"
                # 循环 测试基准数据
                for j in range(count):
                    try:
                        # 开始时间
                        starttime = time.time()
                        result = graphql_Interface(graphql_query, kc)
                        ai_biomind = result['ai_biomind']
                        avgtime = time.time() - starttime
                        avglist.append(avgtime)
                        time.sleep(10)
                    except Exception as e:
                        logger.error("执行预测失败：{0}".format(k.studyuid))
                        continue
                if int(k.diseases) in [9, 12]:
                    jobtype = 'lung_jobJZ'
                    predictiontype ='lung_prediction'
                else:
                    jobtype = 'jobJZ'
                    predictiontype = 'predictionJZ'
                avgtime = str('%.2f' % np.mean(avglist))
                datatest = {
                    "stressid": id,
                    "version": version,
                    "count": count,
                    "modelname": k.diseases,
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
                         ip = serverIP,
                         studyuid = k.studyuid,
                         count =count
                         )

    except Exception as e:
        logger.error("执行预测基准测试数据失败：{0}".format(e))



# 自动预测压测循环
def AutoPrediction(serverID, serverIP, testdata, count):
    # diseases = []
    # for i in testdata.split(","):
    #     diseases.append(i)
    stressdata = stress_record.objects.filter(diseases__in=testdata)
    kc = login_keycloak(serverID)
    for j in stressdata:
        # 检查是否有压测数据
        checkuid(serverID, serverIP, j.stressid)
        delreport(kc, j.studyuid)
    # 循环调用graphql 自动预测
    for i in range(int(count)):
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

            graphql_Interface(graphql_query, kc)
        time.sleep(1)

# 生成自动预测测试数据
def stresscache(stressid):
    obj = stress.objects.get(id=stressid)
    # 循环病种存储 测试数据
    for i in obj.testdata.split(","):
        dictobj = dictionary.objects.get(id=i)
        # 查询预测成功的数据 作为压测数据
        # sql = 'select  DISTINCT studyuid from  prediction_metrics where modelname =\'brainctp\' ORDER BY modelname';
        sql = 'select  DISTINCT studyuid from  prediction_metrics where modelname like \'%{0}%\''.format(dictobj.key)
        results = connect_to_postgres(obj.loadserver, sql).to_dict(orient='records')
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


# 修改数据
def updateStressData(uid, orthanc_ip):
    vote = ''
    Series = connect_to_postgres(orthanc_ip,
                                 "select \"SeriesInstanceUID\" from \"Series\" where \"StudyInstanceUID\" ='{0}'".format(
                                     uid)).to_dict(orient='records')
    pseries_classifier = connect_to_postgres(orthanc_ip,
                                             "select protocol->'pseries_classifier' as \"pseries\" from hanalyticsprotocol where studyuid ='{0}' LIMIT 1;".format(
                                                 uid)).to_dict(orient='records')

    pseries = pseries_classifier[0]['pseries']
    for key in pseries:
        for i in Series:
            if str(i['SeriesInstanceUID']) in str(pseries[key]):
                vote = vote + '{0}: \\"{1}\\",'.format(str(key), str(i['SeriesInstanceUID']))
                SeriesInstanceUID = str(i['SeriesInstanceUID'])
    vote = "{" + vote + "}"
    return str(vote), SeriesInstanceUID


def savecsv(path, graphql_query):
    f = open('{0}'.format(path), 'a', encoding='utf-8', newline="")
    csv_writer = csv.writer(f)
    csv_writer.writerow(graphql_query)
    f.close()


def saveStressddt(id, path):
    obj = stress.objects.get(id=id)
    savecsv('{}/logs/stress/config.csv'.format(path),
            [obj.loadserver, 'biomind3d', 'engine3D.', obj.thread, obj.synchroniz, obj.ramp, time, obj.version,
             obj.loop_count])

    # 循环生成压测数据
    for i in obj.testdata.split(","):
        if int(i) in [4, 7, 8, 10]:
            obd = dictionary.objects.get(id=i)
            sqlobj = dictionary.objects.get(type='sql', key='3d')
            sql = sqlobj.value.format(obd.key, obj.thread)
            stressdict = connect_to_postgres(obj.loadserver, sql)
            stressdata = stressdict.to_dict(orient='records')
        elif int(i) in [9,12]:
            continue
        try:
            for k in stressdata:
                savecsv('{}/logs/stress/data.csv'.format(path, str(i)),
                        [k["publicid"], k["studyinstanceuid"], k["publicid"], k['modality'], obd.remarks])
        except Exception as e:
            continue


# 执行 jmeter 脚本
def jmeterStress(id):
    jmeterobj = uploadfile.objects.filter(fileid=id)
    path = os.path.join(os.getcwd())
    if not os.path.exists('{}/logs/stress'.format(path)):
        os.mkdir('{}/logs/stress'.format(path))
    else:
        shutil.rmtree('{}/logs/stress'.format(path))
        os.mkdir('{}/logs/stress'.format(path))
    saveStressddt(id, path)
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
