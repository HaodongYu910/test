import gc
from TestPlatform.utils.graphql.graphql import *
from TestPlatform.common.regexUtil import connect_to_postgres
from ...utils.keycloak.login_kc import *
from TestPlatform.models import GlobalHost,dictionary

import os,time
import shutil

logger = logging.getLogger(__name__)


from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Avg

from rest_framework.authentication import TokenAuthentication
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
import shutil, threading

from TestPlatform.common.api_response import JsonResponse
from TestPlatform.models import base_data, pid, GlobalHost
from TestPlatform.serializers import duration_Deserializer
from ...tools.dicom.SendDicom import Send
from ...tools.orthanc.deletepatients import *
from ...tools.dicom.duration_verify import *
from ...tools.stress.PerformanceResult import *
from ...tools.orthanc.deletepatients import delete_patients_duration




# 生成csv  数据
def dicomsavecsv(ids):
    path = os.path.join(os.getcwd())
    for i in ids:
        obj = dicom.objects.get(id=i)
        graphql_query = "{ ai_biomind (" \
                        "study_uid:\\\"" + str(obj.studyinstanceuid) + "\\\", protocols:" \
                                                                       "{ pothers: " \
                                                                       "{ disable_negative_voting:false} " \
                                                                       "penable_cached_results:false pconfig:{} " \
                                                                       "planguage:\\\"zh-cn\\\" " \
                                                                       " puser_id:\\\"biomind\\\" " \
                                                                       "pseries_classifier:" + str(obj.vote) + "}" \
                                                                                                               "routes: [[\\\"generate_series\\\",\\\"series_classifier\\\",\\\"" + str(
            obj.predictor) + "\\\"]])" \
                             " { pprediction pmetadata SOPInstanceUID pconfig  pseries_classifier pstatus_code } }"
        if obj.diseases == "Lung":
            diseases = str("{0}_{1}_slicenumber".format(obj.diseases, str(obj.slicenumber)))
        else:
            diseases = obj.diseases
        savecsv(str('{0}/logs/gold.csv'.format(path)), [graphql_query, diseases, obj.diagnosis])

# 正常发送
def normalSend(id):
    obj = duration.objects.get(id=id)
    for i in obj.dicom.split(","):
        try:
            dicomobj = dicom.objects.filter(fileid=str(i))
        except Exception as e:
            continue
        for j in dicomobj:
            delete_patients_duration(j.studyinstanceuid, obj.hostid, 'StudyInstanceUID', False)
        cmd = ('nohup /home/biomind/.local/share/virtualenvs/biomind-dvb8lGiB/bin/python3'
           ' /home/biomind/Biomind_Test_Platform/TestPlatform/tools/dicom/dicomSend.py '
           '--ip {0} --aet {1} '
           '--port {2} '
           '--patientid {3} '
           '--patientname {4} '
           '--folderid {5} '
           '--durationid {6} '
           '--end {7} '
           '--sleepcount {8} '
           '--sleeptime {9} '
           '--series {10} &').format(obj.server, obj.aet, obj.port,'patientid','patientname', i, id,
                                    int(dicomobj.count()), 9999, 1, obj.series)

        logger.info(cmd)
        os.system(cmd)
        time.sleep(1)

    obj.sendstatus = True
    obj.save()

# 匿名化发送数据
def anonymousSend(id, type):
    a = 0
    nom = 0
    try:
        if type != "stress":
            obj = duration.objects.get(id=id)
            sleepcount = obj.sleepcount if obj.sleepcount is not None else 9999
            sleeptime = obj.sleeptime if obj.sleeptime is not None else 0
            if obj.sendcount is None and obj.end_time is None:
                end = 1
            elif obj.sendcount is None and obj.end_time is not None:
                end = (datetime.datetime.now() + datetime.timedelta(hours=int(obj.end_time))).strftime(
                    "%Y-%m-%d %H:%M:%S")
            else:
                for j in obj.dicom.split(","):
                    nom = nom + 1
                imod = divmod(int(obj.sendcount), nom)
                if imod[0] < 1:
                    return JsonResponse(code="999994", msg="少于病种数量，请增加发送数量！")
        else:
            obj = duration.objects.get(id=id)
            sleepcount = 9999
            sleeptime = 0
            end = 500

        for i in obj.dicom.split(","):
            if nom != 0:
                end = int(imod[0]) + int(imod[1]) if a == 0 else int(imod[0])
            a = a + 1
            cmd = ('nohup /home/biomind/.local/share/virtualenvs/biomind-dvb8lGiB/bin/python3'
                   ' /home/biomind/Biomind_Test_Platform/TestPlatform/tools/dicom/dicomSend.py '
                   '--ip {0} --aet {1} '
                   '--port {2} '
                   '--patientid {3} '
                   '--patientname {4} '
                   '--folderid {5} '
                   '--durationid {6} '
                   '--end {7} '
                   '--sleepcount {8} '
                   '--sleeptime {9} '
                   '--series {10} &').format(obj.server, obj.aet, obj.port, obj.patientid,obj.patientname, i, id,
                                            end, sleepcount, sleeptime, obj.series)

            logger.info(cmd)
            os.system(cmd)
            time.sleep(1)

        obj.sendstatus = True
        obj.save()
        return True
    except Exception as e:
        return False
        logger.error("发送失败：{0}".format(e))


# 检查是否数据
def checkuid(serverID, serverIP, dicomid):
    obj = dicom.objects.get(id=dicomid)
    sql = 'select studyinstanceuid,patientname from study_view where studyinstanceuid = \'{0}\''.format(
        obj.studyinstanceuid)
    result_db = connect_to_postgres(serverIP, sql)
    # 无此数据，发送
    if len(result_db) == 0:
        Send(serverID, obj.route)
    # 重复数据 先删除后再发送新数据
    elif len(result_db) > 2:
        delete_patients_duration(obj.studyinstanceuid, serverID, 'StudyInstanceUID', False)
        Send(serverID, obj.route)


# 数据跳转listview url
def listUrl(hostid, studyuid):
    obj = GlobalHost.objects.get(id=hostid)
    kc = login_keycloak(hostid)
    result_db = connect_to_postgres(obj.host,
                                    'select publicid from study_view where studyinstanceuid = \'{0}\''.format(studyuid))

    url = '{0}://{1}/imageViewer/#!/brain?study={2}'.format(obj.protocol, obj.host,result_db["publicid"][0])
    return kc.raw_token,url

def Slice(kc,Seriesuid):
    graphql_query='{ series(SeriesInstanceUID:"' + Seriesuid + '"){ '\
        'NumberOfSeriesRelatedInstances Instances{ SliceThickness } } }'
    graphql = GraphQLDriver('/graphql', kc)
    results = graphql.execute_query(graphql_query)
    if results['series'] == []:
        return False
    elif results['series'][0]['Instances'][0] is None:
        return False
    else:
        imagecount= results['series'][0]['NumberOfSeriesRelatedInstances']
        SliceThickness = round(float(results['series'][0]['Instances'][0]['SliceThickness']), 2)

    return imagecount,SliceThickness

# 查询挂载 张数 层厚
def voteData(uid,orthanc_ip,diseases,kc):
    vote = ''
    try:
        Series = connect_to_postgres(orthanc_ip,
                                     "select \"SeriesInstanceUID\" from \"Series\" where \"StudyInstanceUID\" ='{0}'".format(
                                         uid)).to_dict(orient='records')
        pseries_classifier = connect_to_postgres(orthanc_ip,
                                                 "select protocol->'pseries_classifier' as \"pseries\" from hanalyticsprotocol where studyuid ='{0}' LIMIT 1;".format(
                                                     uid)).to_dict(orient='records')


        pseries = pseries_classifier[0]['pseries']
    except Exception as e:
        logger.info("没有此数据信息{0}".format(e))
        return None,None,None
    try:
        for key in pseries:
            for i in Series:
                if str(i['SeriesInstanceUID']) in str(pseries[key]):
                    vote = vote + '{0}: \"{1}\",'.format(str(key), str(i['SeriesInstanceUID']))
                    SeriesInstanceUID=str(i['SeriesInstanceUID'])
        vote = "{"+vote+"}"

        if int(diseases) in [4,5,7,8,9,10,12]:
            imagecount, slicenumber, = Slice(kc, SeriesInstanceUID)
        else:
            imagecount, slicenumber =None,None
    except Exception as e:
        return None,None,None
    return str(vote),imagecount,slicenumber

