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
from ..tools.dicom.SendDicom import Send
from ..tools.orthanc.deletepatients import *
from ..tools.dicom.duration_verify import *
from ..tools.stress.PerformanceResult import *
from ..tools.orthanc.deletepatients import delete_patients_duration


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
                   '--keyword {3} '
                   '--dicomfolder {4} '
                   '--durationid {5} '
                   '--end {6} '
                   '--sleepcount {7} '
                   '--sleeptime {8} '
                   '--series {9} &').format(obj.server, obj.aet, obj.port, obj.keyword, i, id,
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
def checkuid(serverID, serverIP, studyuid):
    obj = dicom.objects.get(studyinstanceuid=studyuid, type='test')
    sql = 'select studyinstanceuid,patientname from study_view where studyinstanceuid = \'{0}\''.format(
        studyuid)
    result_db = connect_to_postgres(serverIP, sql)
    # 无此数据，发送
    if len(result_db) == 0:
        Send(serverID, obj.route)
    # 重复数据 先删除后再发送新数据
    elif len(result_db) > 2:
        delete_patients_duration(studyuid, serverID, 'StudyInstanceUID', False)
        Send(serverID, obj.route)


# 数据跳转listview url
def listUrl(hostid, studyuid):
    obj = GlobalHost.objects.get(id=hostid)
    kc = login_keycloak(hostid)
    result_db = connect_to_postgres(obj.host,
                                    'select publicid from study_view where studyinstanceuid = \'{0}\''.format(studyuid))

    url = '{0}://{1}/imageViewer/#!/brain?study={2}'.format(obj.protocol, obj.host,result_db["publicid"][0])
    return kc.raw_token,url
