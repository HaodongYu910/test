# coding = utf-8
from TestPlatform.common.PostgreSQL import connect_postgres

from TestPlatform.models import duration_record, duration
from django.db import transaction
from TestPlatform.serializers import duration_record_Deserializer
import logging

logger = logging.getLogger(__name__)


def update_data(data):
    obj = duration_record.objects.get(studyinstanceuid=data["studyinstanceuid"])
    serializer = duration_record_Deserializer(data=data)
    with transaction.atomic():
        if serializer.is_valid():
            serializer.update(instance=obj, validated_data=data)


def ai_result(kc, patientid):
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
    duration_data = duration_record.objects.filter(duration_id=id)
    obj = duration.objects.get(id=id)
    if obj.dds is not None:
        serverip = obj.dds
    else:
        serverip = obj.server
    for i in duration_data:
        if i.imagecount == i.imagecount_server:
            continue
        else:
            data = {'studyinstanceuid': i.studyinstanceuid}
            sql = 'SELECT aistatus,diagnosis,imagecount FROM study_view WHERE studyinstanceuid = \'{0}\' ORDER BY insertiontime desc'.format(
                i.studyinstanceuid)
            result_1 = connect_postgres(host=serverip, sql=sql)
            sqldata = result_1.to_dict(orient='records')

            if sqldata == []:
                continue
            else:
                data['aistatus'] = sqldata[0]['aistatus']
                data['diagnosis'] = sqldata[0]['diagnosis']
                data['imagecount_server'] = sqldata[0]['imagecount']
                if str(data['imagecount_server']) == str(i.imagecount):
                    data['studyolduid'] = '1'
            update_data(data)
    # kc = use_keycloak_bmutils(serverip, 'test', 'Asd@123456')
    # for i in duration_data:
    #     if i.imagecount == i.imagecount_server:
    #         continue
    #     else:
    #         data = {'studyinstanceuid':i.studyinstanceuid}
    #         airesult=ai_result(kc,i.patientid)
    #         if airesult.json()['data']['studyViewFlexible'] ==[]:
    #             continue
    #         else:
    #             # text = eval(str(airesult.content, 'utf-8'), globals)
    #             res_studyView = airesult.json()['data']['studyViewFlexible']
    #             data['aistatus'] = res_studyView[0].get('aistatus')
    #             data['diagnosis'] = res_studyView[0].get('diagnosis')
    #             data['imagecount_server'] = res_studyView[0].get('instancecount')
    #             if str(data['imagecount_server'])==str(i.imagecount):
    #                 data['studyolduid']='1'


def verify():
    duration_data = duration_record.objects.filter()
    for i in duration_data:
        if i.imagecount == i.imagecount_server:
            continue
        else:
            obn = duration.objects.get(id=i.duration_id)
            data = {'studyinstanceuid': i.studyinstanceuid}
            if obn.dds is not None:
                serverip = obn.dds
            else:
                serverip = i.sendserver

            sql = 'SELECT aistatus,diagnosis,imagecount FROM study_view WHERE studyinstanceuid = \'{0}\' ORDER BY insertiontime desc'.format(
                i.studyinstanceuid)
            result_1 = connect_postgres(host=serverip, sql=sql)
            sqldata = result_1.to_dict(orient='records')

            if sqldata == []:
                continue
            else:

                data['aistatus'] = sqldata[0]['aistatus']
                data['diagnosis'] = sqldata[0]['diagnosis']
                data['imagecount_server'] = sqldata[0]['imagecount']
                if str(data['imagecount_server']) == str(i.imagecount):
                    data['studyolduid'] = '1'
            update_data(data)
