import gc
from TestPlatform.utils.graphql.graphql import *
from TestPlatform.common.regexUtil import *
from TestPlatform.models import dicom,base_data,dictionary
from ...utils.graphql.graphql import *
from ..dicom.SendDicom import Send
from ...serializers import dicomrecord_Serializer,dicomrecord_Deserializer
from ...models import dicom_record,dictionary
from ...tools.orthanc.deletepatients import delete_patients_duration
from ...utils.graphql.graphql_ai_status import graphql_ai_status
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
            objbase = base_data.objects.get(id=obj.fileid)
            objdictionary =dictionary.objects.get(id=objbase.predictor)
            data = {
                "version": version,
                "patientid": obj.patientid,
                "server":server_ip,
                "studyinstanceuid": obj.studyinstanceuid,
                "diseases": obj.diseases,
                "slicenumber": obj.slicenumber,
                "diagnosis": obj.diagnosis,
                "type": "Gold",
                "status": True
            }
            sql = 'select studyinstanceuid,patientname from study_view where studyinstanceuid = \'{0}\''.format(
                obj.studyinstanceuid)
            result_db = connect_to_postgres(server_ip, sql)
            # 无此数据，发送
            if len(result_db) == 0:
                Send(server_ip,obj.route)
            # 重复数据 先删除后再发送新数据
            elif len(result_db) > 2:
                delete_patients_duration([i], server_ip,'StudyInstanceUID', False)
                Send(server_ip,obj.route)

            graphql_query = "{ ai_biomind (" \
                            "study_uid:\"" + str(obj.studyinstanceuid) + "\", protocols:" \
                                                                           "{ pothers: " \
                                                                           "{ disable_negative_voting:false} " \
                                                                           "penable_cached_results:false pconfig:{} " \
                                                                           "planguage:\"zh-cn\" " \
                                                                           " puser_id:\"biomind\" " \
                                                                           "pseries_classifier:" + str(obj.vote) + "}" \
                                                                                                                   "routes: [[\"generate_series\",\"series_classifier\",\"" + str(objdictionary.value) + "\"]])" \
                                 " { pprediction pmetadata SOPInstanceUID pconfig  pseries_classifier pstatus_code } }"
            data["starttime"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            # 调用 手动预测接口
            try:
                prediction = graphql_Interface(graphql_query, kc)
            except Exception as e:
                aiFalse(prediction,data)
                continue
            data["completiontime"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            result = graphql_ai_status(str(obj.studyinstanceuid), kc)
            if result is False:
                data["status"] = False
                data["report"] = '预测报错'
                saverecord(data)
                continue
            else:
                checkdata(result,data)
        except Exception as e:
            logger.error("error:{0}".format(e))
            data["report"] = '执行失败'
            data["status"] = False
            saverecord(data)
            continue

def saverecord(data):
    serializer = dicomrecord_Serializer(data=data)
    with transaction.atomic():
        if serializer.is_valid():
            serializer.save()


# 比对 studyView 接口返回值
def checkdata(result,data):
    # 比对结果
    aidiagnosis=''
    try:
        airesult=result['studyView'][0]
        if airesult['aistatus'] in [2,3]:
            data["status"] = True
            if str(airesult['diagnosis']).find(data["diagnosis"]) >= 0:
                aidiagnosis = KeyChange(data["diagnosis"])
                report= '匹配成功'
            elif data["diagnosis"] == 'normal':
                if len(airesult['diagnosis'][0])==0:
                    report = '匹配成功'
                    aidiagnosis = data["diagnosis"]
                else:
                    for i in airesult['diagnosis'][0]:
                        aidiagnosis = KeyChange(str(i)) + ',' + aidiagnosis
                    report = '匹配失败'
            else:
                # 循环取结果
                for i in airesult['diagnosis'][0]:
                    aidiagnosis = KeyChange(str(i)) + ',' + aidiagnosis
                report = '匹配失败'
        else:
            report ='预测失败'
            data["status"] = False
        data["diagnosis"] = KeyChange(data["diagnosis"])
        data["aidiagnosis"] =aidiagnosis
        data["report"] = report
        data["aistatus"] = airesult["aistatus"]
        dicom_record.objects.create(**data)
    except Exception as e:
        data["status"] = False
        data["report"] = '比对失败'
        data["aistatus"] = airesult["aistatus"]

# 预测失败 记录
def aiFalse(result,data):
    data["status"] = False
    data["report"] = '手动预测失败'
    try:
        data["aidiagnosis"] = str(result['ai_biomind']['pstatus_code'][0]['code'])
    except Exception as e:
        logger.error("比对失败:{0},预测结果:{1}".format(e, result['ai_biomind']['pstatus_code']))
    dicom_record.objects.create(**data)
    logger.error("比对失败:{0},预测结果:{1}".format(e, result))

# 预测结论转换
def KeyChange(key):
    try:
        obj =dictionary.objects.get(key__contains=key,type='diseases')
        return obj.value
    except Exception as e:
        logger.error("无此结果:{1}".format(e,key))
        return key

# # 比对预测接口结果
# def checkdata(result,data):
#     # 比对结果
#     aidiagnosis=''
#     try:
#         airesult=result['ai_biomind']['pprediction']
#         if str(airesult).find(data["diagnosis"]) >= 0:
#             data["aidiagnosis"] = data["diagnosis"]
#             data["report"] = '匹配成功'
#             dicom_record.objects.create(**data)
#         else:
#             # 循环取结果
#             for i in airesult.values():
#                 for j in i:
#                     if str(aidiagnosis).find(str(j['classification'])[1:-1]) >= 0:
#                         continue
#                     else:
#                         aidiagnosis =str(j['classification'])[1:-1] + aidiagnosis
#             data["aidiagnosis"] = str(aidiagnosis)
#             data["report"] = '匹配失败'
#             dicom_record.objects.create(**data)
#     except Exception as e:
#         data["status"] = False
#         data["report"] = '比对失败'
#         try:
#             data["aidiagnosis"] = str(result['ai_biomind']['pstatus_code'][0]['code'])
#         except Exception as e:
#             logger.error("比对失败:{0},预测结果:{1}".format(e,result['ai_biomind']['pstatus_code']))
#         dicom_record.objects.create(**data)
#         logger.error("比对失败:{0},预测结果:{1}".format(e,result))


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
