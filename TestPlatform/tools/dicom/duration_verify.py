# coding = utf-8
from TestPlatform.common.regexUtil import *

from TestPlatform.models import duration_record,duration
from django.db import transaction
from TestPlatform.serializers import duration_record_Deserializer,duration_record_Serializer,duration_Serializer
import logging
logger = logging.getLogger(__name__)

def update_data(data):
    obj = duration_record.objects.get(studyinstanceuid=data["studyinstanceuid"])
    serializer = duration_record_Deserializer(data=data)
    with transaction.atomic():
        if serializer.is_valid():
            serializer.update(instance=obj, validated_data=data)

def ai_result(kc,patientid):
    study_query = " \
                    {{\
                      studyViewFlexible(\
                        filter: [\
                          {{ filter: patientname, value: [\"{0}\"],type: FuzzyMatch,category: PatientInfo }}\
                        ]\
                      ) {{\
                        aistatus,\
                        diagnosis,\
                        instancecount\
                      }}\
                    }}".format(patientid)
    res_study = kc.post(
        url='/graphql',
        json={'query': study_query},
        timeout=120,
        verify=False
    )
    return res_study

def verifyData(id):
    today=str(datetime.date.today()) + ' 00:00:00'
    duration_data = duration_record.objects.filter(create_time__gte=today,duration_id=id)
    obj =duration.objects.get(id=id)
    if obj.dds is True:
        serverip = "192.168.1.124"
    else:
        serverip = obj.server
    kc = use_keycloak_bmutils(serverip, 'test', 'Asd@123456')
    for i in duration_data:
        data = {'studyinstanceuid':i.studyinstanceuid}
        airesult=ai_result(kc,i.patientid)
        if airesult.json()['data']['studyViewFlexible'] ==[]:
            continue
        else:
            # text = eval(str(airesult.content, 'utf-8'), globals)
            res_studyView = airesult.json()['data']['studyViewFlexible']
            data['aistatus'] = res_studyView[0].get('aistatus')
            data['diagnosis'] = res_studyView[0].get('diagnosis')
            data['imagecount_server'] = res_studyView[0].get('instancecount')
            if str(data['imagecount_server'])==str(i.imagecount):
                data['studyolduid']='1'
        update_data(data)
    return True

def verify():
    today=str(datetime.date.today()) + ' 00:00:00'
    duration_data = duration_record.objects.filter(create_time__gte=today)

    for i in duration_data:
        data = {'studyinstanceuid':i.studyinstanceuid}
        if i.dds is True:
            serverip="192.168.1.124"
        else:
            serverip=i.sendserver
        kc = use_keycloak_bmutils(serverip, 'test', 'Asd@123456')
        airesult=ai_result(kc,i.patientid)
        if airesult.json()['data']['studyViewFlexible'] ==[]:
            continue
        else:
            # text = eval(str(airesult.content, 'utf-8'), globals)
            res_studyView = airesult.json()['data']['studyViewFlexible']
            data['aistatus'] = res_studyView[0].get('aistatus')
            data['diagnosis'] = res_studyView[0].get('diagnosis')
            data['imagecount_server'] = res_studyView[0].get('instancecount')
            if str(data['imagecount_server']) == str(i.imagecount):
                data['studyolduid']='1'
        update_data(data)
    return True

