import gc
from TestPlatform.utils.graphql.graphql import *
from TestPlatform.common.regexUtil import savecsv,connect_to_postgres
from ...utils.keycloak.login_kc import *
from TestPlatform.models import dicom,base_data,dictionary,smoke
from ...utils.graphql.graphql import *
from ..dicom.SendDicom import Send
from ...serializers import dicomrecord_Serializer,dicomrecord_Deserializer
from ...models import dicom_record,dictionary
from ...tools.orthanc.deletepatients import delete_patients_duration
from ...utils.graphql.graphql_ai_status import graphql_ai_status
from django.db import transaction
import os,datetime

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

def updatesmoke(id,count):
    obj = smoke.objects.get(id=id)
    obj.progress =count
    obj.save()
# 冒烟接口请求
def goldSmoke(id):
    smobj = smoke.objects.get(id=id)

    # for i in obj: ids.append(i.id)
    dicomobj = dicom.objects.filter(fileid__in=smobj.diseases)
    kc = login_keycloak(smobj.hostid)
    Hostobj = GlobalHost.objects.get(id=smobj.hostid)
    serverIP = Hostobj.host
    count = 0
    # 循环测试数据
    for i in dicomobj:
        try:
            count = count + 1
            updatesmoke(id, count)
            objbase = base_data.objects.get(id=i.fileid)
            objdictionary =dictionary.objects.get(id=objbase.predictor)
            data = {
                "version": smobj.version,
                "patientid": i.patientid,
                "server":serverIP,
                "studyinstanceuid": i.studyinstanceuid,
                "diseases": i.diseases,
                "slicenumber": i.slicenumber,
                "diagnosis": i.diagnosis,
                "type": "Gold",
                "status": True,
                "hostid":id
            }
            sql = 'select studyinstanceuid,patientname from study_view where studyinstanceuid = \'{0}\''.format(
                i.studyinstanceuid)
            result_db = connect_to_postgres(serverIP, sql)
            # 无此数据，发送
            if len(result_db) == 0:
                Send(smobj.hostid,i.route)
            # 重复数据 先删除后再发送新数据
            elif len(result_db) > 2:
                delete_patients_duration([i], serverIP,'StudyInstanceUID', False)
                Send(smobj.hostid,i.route)

            graphql_query = "{ ai_biomind (" \
                            "study_uid:\"" + str(i.studyinstanceuid) + "\", protocols:" \
                                                                           "{ pothers: " \
                                                                           "{ disable_negative_voting:false} " \
                                                                           "penable_cached_results:false pconfig:{} " \
                                                                           "planguage:\"zh-cn\" " \
                                                                           " puser_id:\"biomind\" " \
                                                                           "pseries_classifier:" + str(i.vote) + "}" \
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
            result = graphql_ai_status(str(i.studyinstanceuid), kc)
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


# 删除dicom报告
def delreport(serverID, ids):
    kc = login_keycloak(serverID)
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
