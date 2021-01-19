from TestPlatform.common.regexUtil import savecsv,connect_to_postgres
from ...utils.keycloak.login_kc import *
from TestPlatform.models import dicom,base_data,dictionary,smoke
from ...utils.graphql.graphql import *
from ..dicom.SendDicom import Send
from ...models import smoke_record,dictionary
from ...tools.orthanc.deletepatients import delete_patients_duration
from ...utils.graphql.graphql_ai_status import graphql_ai_status
from django.db import transaction
import os,datetime

logger = logging.getLogger(__name__)

# 修改执行进度
def updatesmoke(id,count):
    obj = smoke.objects.get(id=id)
    obj.progress =count
    obj.save()

# 验证测试数据
def datacheck(serverIP,uid,route,hostid):

    sql = 'select studyinstanceuid,patientname from study_view where studyinstanceuid = \'{0}\''.format(
        uid)
    result_db = connect_to_postgres(serverIP, sql)
    # 无此数据，发送
    if len(result_db) == 0:
        Send(hostid,route)
    # 重复数据 先删除后再发送新数据
    elif len(result_db) > 2:
        delete_patients_duration(uid, serverIP, 'StudyInstanceUID', False)
        Send(hostid,route)


# 冒烟接口请求
def goldSmoke(id):
    # for i in obj: ids.append(i.id)
    count = 0
    smobj = smoke.objects.get(id=id)
    smobj.starttime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    kc = login_keycloak(smobj.hostid)
    Hostobj = GlobalHost.objects.get(id=smobj.hostid)
    serverIP = Hostobj.host
    # 循环测试数据
    for k in smobj.diseases.split(","):
        try:
            dicomobj = dicom.objects.filter(fileid=k.strip())
        except Exception as e:
            logger.error("数据错误")
            continue
        for i in dicomobj:
            try:
                # 验证数据cunz
                datacheck(serverIP,i.studyinstanceuid,i.route,smobj.hostid)
                # 修改执行进度
                count = count + 1
                updatesmoke(id, count)
                objbase = base_data.objects.get(id=i.fileid)
                objdictionary =dictionary.objects.get(id=objbase.predictor)
                data = {
                    "version": smobj.version,
                    "patientid": i.patientid,
                    "patientname": i.patientname,
                    "studyinstanceuid": i.studyinstanceuid,
                    "diseases": i.diseases,
                    "slicenumber": i.slicenumber,
                    "diagnosis": i.diagnosis,
                    "type": "gold",
                    "status": False,
                    "smokeid":id
                }
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
                    predictionCheck(prediction,data,e)
                    continue
                data["completiontime"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                Check = predictionCheck(prediction,data,'')
                if Check is True:
                    checkdata(data, kc)
            except Exception as e:
                logger.error("error:{0}".format(e))
                data["result"] = str(e)[:500]
                smoke_record.objects.create(**data)
                continue
    smobj.completiontime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    smobj.save()

# 比对 studyView 接口返回值
def checkdata(data,kc):
    aidiagnosis = ''
    result = graphql_ai_status(data["studyinstanceuid"], kc)
    if result is False:
        data["result"] = '查询预测结果报错'
    else:
        try: # 比对结果
            airesult=result['studyView'][0]
            if airesult['aistatus'] in [2,3]:
                data["status"] = True
                if str(airesult['diagnosis']).find(data["diagnosis"]) >= 0:
                    aidiagnosis = KeyChange(data["diagnosis"])
                    data["result"]= '匹配成功'
                elif data["diagnosis"] == 'normal':
                    if len(airesult['diagnosis'][0])==0:
                        data["result"] = '匹配成功'
                        aidiagnosis = data["diagnosis"]
                    else:
                        for i in airesult['diagnosis'][0]:
                            aidiagnosis = KeyChange(str(i)) + ',' + aidiagnosis
                        data["result"] = '匹配失败'
                else:
                    # 循环取结果
                    for i in airesult['diagnosis'][0]:
                        aidiagnosis = KeyChange(str(i)) + ',' + aidiagnosis
                    data["result"] = '匹配失败'
            else:
                data["result"] = str(result)[:500]
        except Exception as e:
            data["result"]=str(e)[:1000]
    data["diagnosis"] = KeyChange(data["diagnosis"])
    data["aidiagnosis"] = aidiagnosis
    data["aistatus"] = airesult["aistatus"]
    smoke_record.objects.create(**data)

# 预测验证记录
def predictionCheck(result,data,error):
    data["aidiagnosis"] = ''
    try:
        ai_biomind =result['ai_biomind']
        try:
            data["result"] = str(ai_biomind['pstatus_code'][0]['code'])
            smoke_record.objects.create(**data)
        except Exception as e:
            return True
    except Exception as e:
        data["result"] = str(error)[:500]
        smoke_record.objects.create(**data)
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
def delresult(serverID, ids):
    kc = login_keycloak(serverID)
    # 循环删除数据报告
    for i in ids:
        try:
            obj = dicom.objects.get(id=i)
            graphql_query = 'mutation{ ' \
                            'deleteresult( studyuid:' + str(obj.studyinstanceuid) + ' )' \
                                                                                    'deleteProtocol( studyuid:' + str(
                obj.studyinstanceuid) + ' ) }'
            graphql_Interface(graphql_query, kc)
        except:
            logger.error("删除失败{0}".format(obj.studyinstanceuid))
            continue
