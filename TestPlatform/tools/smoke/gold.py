import gc
from TestPlatform.utils.graphql.graphql import *
from TestPlatform.common.regexUtil import *
from TestPlatform.models import dicom
from ...utils.graphql.graphql import *
from ..dicom.SendDicom import Send
from ...serializers import dicomrecord_Serializer,dicomrecord_Deserializer
from ...models import dicom_record
from django.db import transaction
import os

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

# 冒烟接口请求
def goldSmoke(version, server_ip, ids):
    kc = use_keycloak_bmutils(server_ip, 'test', 'Asd@123456')
    # 循环测试数据
    for i in ids:
        try:
            obj = dicom.objects.get(id=i)
            data = {
                "version": version,
                "patientid": obj.patientid,
                "studyinstanceuid": obj.studyinstanceuid,
                "diseases": obj.diseases,
                "slicenumber": obj.slicenumber,
                "diagnosis": obj.diagnosis,
                "type": "Gold",
                "status": True
            }
            sql = 'select studyinstanceuid from study_view where studyinstanceuid = \'{0}\''.format(
                obj.studyinstanceuid)
            result_db = connect_to_postgres(server_ip, sql)

            if len(result_db) == 0:
                Send(server_ip, i, '')
            elif len(result_db) > 1:
                delreport(server_ip, [i])
                Send(server_ip, i, '')

            graphql_query = "{ ai_biomind (" \
                            "study_uid:\"" + str(obj.studyinstanceuid) + "\", protocols:" \
                                                                           "{ pothers: " \
                                                                           "{ disable_negative_voting:false} " \
                                                                           "penable_cached_results:false pconfig:{} " \
                                                                           "planguage:\"zh-cn\" " \
                                                                           " puser_id:\"biomind\" " \
                                                                           "pseries_classifier:" + str(obj.vote) + "}" \
                                                                                                                   "routes: [[\"generate_series\",\"series_classifier\",\"" + str(
                obj.predictor) + "\"]])" \
                                 " { pprediction pmetadata SOPInstanceUID pconfig  pseries_classifier pstatus_code } }"
            data["starttime"] = datetime.datetime.now().strftime("%Y-%m-%d%H%M%S")
            result = graphql_Interface(graphql_query, kc)
            data["completiontime"] = datetime.datetime.now().strftime("%Y-%m-%d%H%M%S")
            if result is False:
                data["status"] = False
                data["report"] = '预测失败'
                saverecord(data)
                continue
            else:
                checkdata(result,data)
        except Exception as e:
            logger.error("error:{0}".format(e))
            data["report"] = '数据问题'
            data["status"] = False
            saverecord(data)
            continue

def saverecord(data):
    serializer = dicomrecord_Serializer(data=data)
    with transaction.atomic():
        if serializer.is_valid():
            serializer.save()


# # 比对结果
def checkdata(result,data):
    # 比对结果
    aidiagnosis=''
    try:
        airesult=result['ai_biomind']['pprediction']
        if str(airesult).find(data["diagnosis"]) >= 0:
            data["aidiagnosis"] = data["diagnosis"]
            data["report"] = '匹配成功'
            dicom_record.objects.create(**data)
        else:
            for i in airesult.values():
                for j in i:
                    aidiagnosis =str(j['classification']) + aidiagnosis
            data["aidiagnosis"] = str(aidiagnosis)
            data["report"] = '匹配失败'
            dicom_record.objects.create(**data)
    except Exception as e:
        data["status"] = False
        data["report"] = '比对失败'
        dicom_record.objects.create(**data)
        logger.error("比对失败:{0},预测结果:{1}".format(e,result))


# 删除dicom报告
def delreport(server_ip, ids):
    kc = use_keycloak_bmutils(server_ip, 'test', 'Asd@123456')
    # 循环删除数据报告
    for i in ids:
        try:
            obj = dicom.objects.get(id=i)
            graphql_query = 'mutation{ ' \
                            'deleteReport( studyuid:' + str(obj.studyinstanceuid) + ' )' \
                                                                                    'deleteProtocol( studyuid:' + str(
                obj.studyinstanceuid) + ' ) }'
            graphql_Interface(graphql_query, kc)
        except:
            logger.error("删除失败{0}".format(obj.studyinstanceuid))
            continue
