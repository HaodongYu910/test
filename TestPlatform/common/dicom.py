from rest_framework.authentication import TokenAuthentication
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
import shutil,threading

from TestPlatform.common.api_response import JsonResponse
from TestPlatform.models import base_data, pid, GlobalHost
from TestPlatform.serializers import duration_Deserializer
from ..tools.dicom.anonymization import onlyDoAnonymization
from ..tools.orthanc.deletepatients import *
from ..tools.dicom.duration_verify import *
from ..tools.stress.PerformanceResult import *




def dicomSend():
    try:
        a = 0
        nom = 0
        durationid = data["id"]
        obj = duration.objects.get(id=durationid)
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
                   '--series {9} &').format(obj.server, obj.aet, obj.port, obj.keyword, i, durationid,
                                            end, sleepcount, sleeptime, obj.series)

            logger.info(cmd)
            os.system(cmd)
            time.sleep(1)