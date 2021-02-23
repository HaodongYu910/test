from TestPlatform.utils.graphql.graphql import *
from ...utils.keycloak.login_kc import *
from TestPlatform.common.api_response import JsonResponse
from TestPlatform.models import base_data, pid, GlobalHost, stress, dictionary, dicom
from TestPlatform.serializers import duration_Deserializer
from ...tools.dicom.SendDicom import Send
from ...tools.dicom.duration_verify import *
from ...tools.stress.PerformanceResult import savecsv
from ...tools.orthanc.deletepatients import delete_patients_duration
import shutil

logger = logging.getLogger(__name__)


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
            dicomobj = dicom.objects.filter(fileid=str(i), status=True)
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
               '--series {10} &').format(obj.server, obj.aet, obj.port, 'patientid', 'patientname', i, id,
                                         int(dicomobj.count()), 9999, 1, obj.series)

        logger.info(cmd)
        os.system(cmd)
        time.sleep(1)

    obj.sendstatus = True
    obj.save()


# 匿名化发送数据
def anonymousSend(id,type):
    a = 0
    nom = 0
    try:
        # 持续话匿名发送数据
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
                       '--series {10} &').format(obj.server, obj.aet, obj.port, obj.patientid, obj.patientname, i, id,
                                                 end, sleepcount, sleeptime, obj.series)
                logger.info(cmd)
                os.system(cmd)
                time.sleep(1)
        # 性能发送数据
        else:
            obj = stress.objects.get(id=id)
            hostobj = GlobalHost.objects.get(id=obj.hostid)
            for i in range(int(obj.ramp)):
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
                       '--series {10} &').format(hostobj.host, hostobj.description, hostobj.port,"stress{}".format(i),"stress{}".format(i),obj.testdata, '0{}'.format(id),
                                                 int(obj.loop_count),8787,0,0)
                os.system(cmd)
                logger.info(cmd)
        obj.sendstatus = True
        obj.save()
        return True
    except Exception as e:
        return False
        logger.error("发送失败：{0}".format(e))


def durationStop(durationid):
    # 查找pid
    okj = duration.objects.get(id=durationid)
    # 改变状态
    okj.sendstatus = False
    okj.save()
    drobj = duration_record.objects.filter(duration_id=durationid, imagecount=None)
    # 删除错误数据
    for j in drobj:
        delete_patients_duration(j.studyinstanceuid, okj.hostid, "studyinstanceuid", False)
    drobj.delete()
    # 删除 文件夹
    folder = "/home/biomind/Biomind_Test_Platform/logs/{0}{1}{2}".format(str(okj.patientname), str(okj.patientid),
                                                                         str(okj.id))
    if os.path.exists(folder):
        shutil.rmtree(folder)

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

    url = '{0}://{1}/imageViewer/#!/brain?study={2}'.format(obj.protocol, obj.host, result_db["publicid"][0])
    return kc.raw_token, url


def Slice(kc, Seriesuid):
    graphql_query = '{ series(SeriesInstanceUID:"' + Seriesuid + '"){ ' \
                                                                 'NumberOfSeriesRelatedInstances Instances{ SliceThickness } } }'
    graphql = GraphQLDriver('/graphql', kc)
    results = graphql.execute_query(graphql_query)
    if results['series'] == []:
        return None,None
    else:
        try:
            imagecount = results['series'][0]['NumberOfSeriesRelatedInstances']
        except Exception as e:
            imagecount = None
        try:
            SliceThickness = round(float(results['series'][0]['Instances'][0]['SliceThickness']), 2)
        except Exception as e:
            SliceThickness = None
    return imagecount, SliceThickness


# 查询挂载 张数 层厚
def voteData(uid, orthanc_ip, diseases, kc):
    vote = ''
    version ='new'
    try:
        if version =="old":
            Series = 'select "SeriesInstanceUID" as "seriesinstanceuid" from "Series" where "StudyInstanceUID" =\'{0}\''
        else:
            Series = dictionary.objects.get(type='sql', key='Series').value
        protocol = dictionary.objects.get(type='sql', key='protocol')
        Series = connect_to_postgres(orthanc_ip, Series.format(uid)).to_dict(orient='records')
        pseries_classifier = connect_to_postgres(orthanc_ip, protocol.value.format(uid)).to_dict(orient='records')
        pseries = pseries_classifier[0]['pseries']
    except Exception as e:
        logger.info("没有此数据信息{0}".format(e))
        return None, None, None
    try:
        for key in pseries:
            if key in ["Breast_DWI", "Breast_AX_T1", "DCE", "Breast_AX_T2", "CINE_SHORT", "CINE_2CH", "CINE_3CH",
                       "CINE_4CH", "LGE_SHORT", "AX_T1", "AX_T2", "AX_TC", "DWI_B1000", "ADC", "AX_T2Flair", "SWI",
                       "T2_STAR","CT_Lung","CT_Brain","CTA","CT_120KV","CTP"]:
                for i in Series:
                    if str(i['seriesinstanceuid']) in str(pseries[key]):
                        vote = vote + '{0}: \"{1}\",'.format(str(key), str(i['seriesinstanceuid']))
                        SeriesInstanceUID = str(i['seriesinstanceuid'])
        if int(diseases) in [4, 5, 8, 9, 10, 12]:
            imagecount, slicenumber, = Slice(kc, SeriesInstanceUID)
        else:
            imagecount, slicenumber = None, None
        vote = "{" + vote + "}"
    except Exception as e:
        return vote, None, None
    return str(vote), imagecount, slicenumber

# 生成graphql 接口 json
def graphql_query(studyuid,vote,predictorid,predictor):
    if str(predictorid) in ["9", "6", "8"]:
        manager = "\",\"artifacts_manager\"]])"
    else:
        manager = "\"]])"

    graphql_query = "{ ai_biomind (" \
                    "study_uid:\"" + str(studyuid) + "\", protocols:" \
                                                               "{ pothers: " \
                                                               "{ disable_negative_voting:false} " \
                                                               "penable_cached_results:false pconfig:{} " \
                                                               "planguage:\"zh-cn\" " \
                                                               " puser_id:\"biomind\" " \
                                                               "pseries_classifier:" + str(vote) + "}" \
                  "routes: [[\"generate_series\",\"series_classifier\",\"" + str(
        predictor) + manager + "{ pprediction pmetadata SOPInstanceUID pconfig  pseries_classifier pstatus_code } }"
    logger.info("请求graphql_query：{0}".format(graphql_query))
    return graphql_query