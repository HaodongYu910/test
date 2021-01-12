from TestPlatform.models import dicom_record, dictionary, stress_record, stress_result,uploadfile,stress
from django.db import transaction
from TestPlatform.serializers import dicomrecord_Serializer
from ..dicom.dicomdetail import voteData
from ..stress.PerformanceResult import saveResult
from .PerformanceResult import lung
from ..dicom.dicomdetail import checkuid
from ...utils.keycloak.login_kc import *
from TestPlatform.utils.graphql.graphql import *
from TestPlatform.common.regexUtil import *
import os,time
import shutil

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


# 手动预测
def Manual(serverID,serverIP,version,id):

    kc = login_keycloak(serverID)
    stressdata = stress_record.objects.filter(benchmarkstatus=True,status=True)
    imagecount =''
    slicenumber =''
    try:
        startdate = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        for k in stressdata:
            checkuid(serverID,serverIP, str(k.stressid))
            starttime = time.time()
            obj = dictionary.objects.get(id=k.diseases)
            graphql_query = "{ ai_biomind (" \
                            "study_uid:\"" + str(k.studyuid) + "\", protocols:" \
                                                                         "{ pothers: " \
                                                                         "{ disable_negative_voting:false} " \
                                                                         "penable_cached_results:false pconfig:{} " \
                                                                         "planguage:\"zh-cn\" " \
                                                                         " puser_id:\"biomind\" " \
                                                                         "pseries_classifier:" + str(k.graphql) + "}" \
                                                                         "routes: [[\"generate_series\",\"series_classifier\",\"" + str(obj.value) + "\"]])" \
                                       " { pprediction pmetadata SOPInstanceUID pconfig  pseries_classifier pstatus_code } }"
            try:
                graphql_Interface(graphql_query, kc)
            except Exception as e:
                logger.error("执行预测失败：{0}".format(k.studyuid))
                continue
            avgtime = time.time() - starttime

            if int(k.diseases) in [4,5,7,8,10,9]:
                vote, imagecount, slicenumber = voteData(k.studyuid, serverIP, int(k.diseases))
            data ={
                "stressid":id,
                "version": version,
                "type": "jobJZ",
                "count":1,
                "modelname":k.diseases,
                "slicenumber":slicenumber,
                "avg":str('%.2f' % avgtime),
                "single":str('%.2f' % avgtime),
                "median": str('%.2f' % avgtime),
                "min": str('%.2f' % avgtime),
                "max":str('%.2f' % avgtime),
                "minimages":imagecount,
                "maximages": imagecount,
                "avgimages": imagecount,
            }
            stress_result.objects.create(**data)
        enddate =datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    except Exception as e:
        logger.error("执行预测基准测试数据失败：{0}".format(e))
    try:
        sql = dictionary.objects.get(key='prediction', type='sql')
        strsql = sql.value.format(startdate,enddate)
        saveResult(serverIP,version,'predictionJZ',[startdate,enddate],strsql,[])
        lung([startdate,enddate], serverIP,version, 9)
    except Exception as e:
        logger.error("保存预测基准测试数据失败：{0}".format(e))

# 自动预测压测循环
def AutoPrediction(serverID,serverIP,testdata,count):
    diseases=[]
    for i in testdata.split(","):
        diseases.append(i)
    stressdata = stress_record.objects.filter(diseases__in=testdata)
    kc = login_keycloak(serverID)
    # 检查是否有压测数据
    for k in stressdata:
        checkuid(serverID,serverIP, k.stressid)
        delreport(kc, k.studyuid)
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
            time.sleep(2)
            # info[k.slicenumber] = info[k.slicenumber] + 1


# 生成自动预测测试数据
def stresscache(stressid):
    obj = stress.objects.get(id=stressid)
    # 循环病种存储 测试数据
    for i in obj.testdata.split(","):
        dictobj = dictionary.objects.get(id =i)
        # 查询预测成功的数据 作为压测数据
        # sql = 'select  DISTINCT studyuid from  prediction_metrics where modelname =\'brainctp\' ORDER BY modelname';
        sql = 'select  DISTINCT studyuid from  prediction_metrics where modelname like \'%{0}%\''.format(dictobj.key)
        results = connect_to_postgres(obj.loadserver, sql).to_dict(orient='records')
        # 循环插入数据
        for j in results:
            logger.info(j['studyuid'])
            # graphql_query, imagecount, slicenumber=None,None,None
            graphql_query, imagecount, slicenumber = voteData(j['studyuid'], obj.loadserver,int(i))
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
                SeriesInstanceUID=str(i['SeriesInstanceUID'])
    vote = "{" + vote + "}"
    return str(vote),SeriesInstanceUID


def savecsv(path, graphql_query):
    f = open('{0}'.format(path), 'a', encoding='utf-8', newline="")
    csv_writer = csv.writer(f)
    csv_writer.writerow(graphql_query)
    f.close()

# 执行 jmeter 脚本
def jmeterStress(id):
    obj = stress.objects.get(id=id)
    jmeterobj = uploadfile.objects.filter(fileid=id)
    path = os.path.join(os.getcwd())
    if not os.path.exists('/home/biomind/logs/stressdata'):
        os.mkdir('/home/biomind/logs/stressdata')
    else:
        shutil.rmtree('/home/biomind/logs/stressdata')
        os.mkdir('/home/biomind/logs/stressdata')
    list=[obj.loadserver, 'test', 'Asd@123456', obj.thread, obj.synchroniz, obj.ramp, time, obj.version,obj.loop_count]
    savecsv('/home/biomind/logs/stressdata/config.csv'.format(path),list)

    # 循环生成压测数据
    for i in [4,7,8,10]:
        obd = dictionary.objects.get(id=i)
        sqlobj =dictionary.objects.get(type='sql',key='3d')
        sql =sqlobj.value.format(obd.key,obj.thread)
        stressdata = connect_to_postgres(obj.loadserver,sql)

        for k in stressdata.to_dict(orient='records'):
            savecsv('/home/biomind/logs/stressdata/data.csv'.format(path, str(i)), [k["publicid"],k["studyinstanceuid"],k["publicid"],k['modality'],obd.remarks])
    # 执行jmeter
    try:
        for j in jmeterobj:
            start_time = datetime.datetime.now().strftime("%Y-%m-%d%H%M%S")
            cmd = 'nohup jmeter -n -t {0}/{1} -l /home/biomind/logs/{2}.jtl -j /home/biomind/logs/jmeter{3}.log &'.format(j.fileurl, j.filename,start_time,start_time)
            logger.info(cmd)
            os.system(cmd)
    except Exception as e:
        logger.error("执行jmeter失败{0}".format(e))
