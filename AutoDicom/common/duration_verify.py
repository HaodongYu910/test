# coding = utf-8
from AutoTest.common.PostgreSQL import connect_postgres
from ..models import duration_record, duration
from AutoTest.models import Server
import logging

logger = logging.getLogger(__name__)


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

#  duration 数据结果更新
def verifyDuration(durationid):
    duration_data = duration_record.objects.filter(duration_id=durationid, aistatus=None)
    obj = duration.objects.get(id=durationid)
    if obj.dds is not None:
        serID = Server.objects.get(host=obj.dds).id
    else:
        serID = obj.Host.id
    for i in duration_data:
        data = {'studyinstanceuid': i.studyinstanceuid}
        sql = 'SELECT aistatus,diagnosis,imagecount FROM study_view WHERE studyinstanceuid = \'{0}\' ORDER BY insertiontime desc'.format(
            i.studyinstanceuid)
        result_1 = connect_postgres(host=serID, sql=sql, database="orthanc")
        sqldata = result_1.to_dict(orient='records')

        if sqldata == []:
            continue
        else:
            i.aistatus = sqldata[0]['aistatus']
            i.diagnosis = sqldata[0]['diagnosis']
            i.imagecount_server = sqldata[0]['imagecount']
            i.save()

