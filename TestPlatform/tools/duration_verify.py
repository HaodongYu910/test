# coding = utf-8
from TestPlatform.common.regexUtil import *

from TestPlatform.models import duration_record,duration
from django.db import transaction
from TestPlatform.serializers import duration_record_Deserializer,duration_record_Serializer,duration_Serializer


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

def verify():
    duration_data = duration_record.objects.filter(aistatus__isnull=True)
    for i in duration_data:
        data = {'studyinstanceuid':i.studyinstanceuid}
        if i.sendserver=="192.168.1.228":
            serverip="192.168.1.124"
        else:
            serverip=i.sendserver
        kc = use_keycloak_bmutils(serverip, 'biomind', 'password')
        airesult=ai_result(kc,i.patientid)
        if airesult.json()['data']['studyViewFlexible'] ==[]:
            data['aistatus']= None
            data['diagnosis'] = None
            data['instancecount'] = None
        else:
            # text = eval(str(airesult.content, 'utf-8'), globals)
            res_studyView = airesult.json()['data']['studyViewFlexible']
            data['aistatus'] = res_studyView[0].get('aistatus')
            data['diagnosis'] = res_studyView[0].get('diagnosis')
            data['imagecount_server'] = res_studyView[0].get('instancecount')
        update_data(data)
    return True

def verifydata():
    datalist=[]

    def getYesterday():
        today = datetime.date.today()
        oneday = datetime.timedelta(days=1)
        yesterday = today - oneday
        return yesterday
    yesterday =str(getYesterday()) +' 00:00:00'
    for i in duration.objects.filter():
        duration_all = duration_record.objects.filter(duration_id=i.id,create_time__lte=yesterday)
        duration_true = duration_record.objects.filter(aistatus__isnull=False,duration_id=i.id,create_time__lte=yesterday)
        duration_ai_true= duration_record.objects.filter(aistatus=1,duration_id=i.id,create_time__lte=yesterday)
        duration_ai_false = duration_record.objects.filter(aistatus__in=[0,-1,-2,2], duration_id=i.id,
                                                        create_time__lte=yesterday)
        data = {
            'id' :i.id,
            'all':duration_all.count(),
            'duration_true': duration_true.count(),
            'ai_true': duration_ai_true.count(),
            'ai_false': duration_ai_false.count(),
        }
        datalist.append(data)

    return datalist

