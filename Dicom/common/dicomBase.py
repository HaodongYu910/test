from TestPlatform.models import base_data
from AutoUI.models import auto_uicase
from .Dicom import Send
from .deletepatients import *
from .duration_verify import *
from .deletepatients import delete_patients_duration


# id 转换成病种文案
def baseTransform(basedata, basetype):
    result = ''
    try:
        for i in basedata.split(","):
            if basetype == 'base':
                obj = base_data.objects.get(id=i)
                result = result + obj.remarks + ","
            elif basetype == 'dictionary':
                obj = dictionary.objects.get(id=i)
                result = result + obj.value + ","
            elif basetype == 'host':
                obj = GlobalHost.objects.get(id=i)
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
