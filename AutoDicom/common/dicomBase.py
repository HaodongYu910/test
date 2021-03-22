from ..models import dicom_base, dicom
from AutoUI.models import auto_uicase
from .deletepatients import *
from .deletepatients import delete_patients_duration
from AutoTest.utils.graphql.graphql import *
from AutoTest.utils.keycloak.login_kc import *

from AutoTest.models import Server, dictionary
from .Dicom import Send
from .duration_verify import *
from AutoTest.common.PostgreSQL import connect_postgres
from AutoTest.common.regexUtil import savecsv
import os


logger = logging.getLogger(__name__)


# id 转换成病种文案
def baseTransform(basedata, basetype):
    result = ''
    try:
        for i in basedata.split(","):
            if basetype == 'base':
                obj = dicom_base.objects.get(id=i)
                result = result + obj.remarks + ","
            elif basetype == 'dictionary':
                obj = dictionary.objects.get(id=i)
                result = result + obj.value + ","
            elif basetype == 'host':
                obj = Server.objects.get(id=i)
                result = obj.host
            elif basetype == 'case':
                obj = auto_uicase.objects.get(caseid=i)
                result = result + obj.name + ","
        return result
    except Exception as e:
        return 'None'
        logger.error("发送失败：{0}".format(e))


# 检查是否数据
def checkuid(serverID, serverIP, studyuid):
    obj = dicom.objects.get(studyinstanceuid=studyuid, type='test')
    sql = 'select studyinstanceuid,patientname from study_view where studyinstanceuid = \'{0}\''.format(
        studyuid)
    result_db = connect_postgres(host=serverIP, sql=sql)
    # 无此数据，发送
    if len(result_db) == 0:
        Send(serverID, obj.route)
    # 重复数据 先删除后再发送新数据
    elif len(result_db) > 2:
        delete_patients_duration(studyuid, serverID, 'StudyInstanceUID', False)
        Send(serverID, obj.route)


#  duration 统计数据
def durationtotal(durationid):
    notsent = duration_record.objects.filter(duration_id=durationid, aistatus=None)
    ai_true = duration_record.objects.filter(duration_id=durationid, aistatus__in=['1', '2'])
    ai_false = duration_record.objects.filter(duration_id=durationid, aistatus__in=['3', '-2'])
    notai = duration_record.objects.filter(duration_id=durationid, aistatus__in=['-1'])
    datalist = {
        'notai': notai.count(),
        'ai_true': ai_true.count(),
        'ai_false': ai_false.count(),
        'notsent': notsent.count()
    }
    return datalist


#  duration 数据结果更新
def verifyDuration(durationid):
    duration_data = duration_record.objects.filter(duration_id=durationid, aistatus=None)
    obj = duration.objects.get(id=durationid)
    if obj.dds is not None:
        serverip = obj.dds
    else:
        serverip = obj.server
    for i in duration_data:
        data = {'studyinstanceuid': i.studyinstanceuid}
        sql = 'SELECT aistatus,diagnosis,imagecount FROM study_view WHERE studyinstanceuid = \'{0}\' ORDER BY insertiontime desc'.format(
            i.studyinstanceuid)
        result_1 = connect_postgres(host=serverip, sql=sql)
        sqldata = result_1.to_dict(orient='records')

        if sqldata == []:
            continue
        else:
            i.aistatus = sqldata[0]['aistatus']
            i.diagnosis = sqldata[0]['diagnosis']
            i.imagecount_server = sqldata[0]['imagecount']
            i.save()


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



# 匿名化发送数据





# 检查是否数据
def checkuid(serverID, serverIP, dicomid):
    obj = dicom.objects.get(id=dicomid)
    sql = 'select studyinstanceuid,patientname from study_view where studyinstanceuid = \'{0}\''.format(
        obj.studyinstanceuid)
    result_db = connect_postgres(host=serverIP, sql=sql)
    # 无此数据，发送
    if len(result_db) == 0:
        Send(serverID, obj.route)
    # 重复数据 先删除后再发送新数据
    elif len(result_db) > 2:
        delete_patients_duration(obj.studyinstanceuid, serverID, 'StudyInstanceUID', False)
        Send(serverID, obj.route)


# 数据跳转listview url
def listUrl(hostid, studyuid):
    obj = Server.objects.get(id=hostid)
    kc = login_keycloak(hostid)
    result_db = connect_postgres(host=obj.host,
                                    sql='select publicid from study_view where studyinstanceuid = \'{0}\''.format(studyuid))

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
        Series = connect_postgres(host=orthanc_ip, sql=Series.format(uid)).to_dict(orient='records')
        pseries_classifier = connect_postgres(host=orthanc_ip, sql=protocol.value.format(uid)).to_dict(orient='records')
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