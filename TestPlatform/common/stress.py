# from TestPlatform.utils.graphql.get_graphql_result import get_graphql_result
from ..utils.graphql.graphql_prediction import graphql_Interface
from TestPlatform.common.regexUtil import *
from TestPlatform.models import stress_detail_record, stress_data
from django.db import transaction
from TestPlatform.serializers import stressdetail_Serializer, stressdetail_Deserializer
import datetime
import threading
from ..tools.duration_send import stress_duration


# 修改数据
def update_data(data):
    obj = stress_detail_record.objects.get(testid=data["testid"])
    serializer = stressdetail_Deserializer(data=data)
    with transaction.atomic():
        if serializer.is_valid():
            serializer.update(instance=obj, validated_data=data)


#
def graphql_prediction(data, kc):
    try:
        start_time = time.time()
        results = graphql_Interface(data, 'ai', kc)
        data['duration'] = time.time() - start_time
        # data['report'] = str(results['ai_biomind']['preport'])
        stress_detailserializer = stressdetail_Serializer(data=data)
        with transaction.atomic():
            stress_detailserializer.is_valid()
            stress_detailserializer.save()
    except Exception as e:
        logging.error('Query failed: {0}'.format(e))
        return e
    return True


def sequence(orthanc_ip,end_time, diseases, version,duration,keyword):
    loop =0
    if duration =='True':
        server_port=''
        server_aet ='ORTHANC208'
        for i in diseases:
            threading.Thread(target=stress_duration, args=(orthanc_ip,server_port,server_aet,keyword,i,end_time)).start()
            # stress_duration(orthanc_ip,server_port,server_aet,keyword,i,end_time)
            time.sleep(1)
    kc = use_keycloak_bmutils(orthanc_ip, "biomind", "password")
    stressdata = stress_data.objects.filter()

    while datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") <= end_time:
        """Execute Test sequence."""
        loop =loop+1
        for k in stressdata:
            if k.diseases in diseases:
                data = {"version": version,
                        "testid": version + k.studyinstanceuid + str(loop),
                        "patientid": k.patientid,
                        "studyinstanceuid": k.studyinstanceuid,
                        "vote":k.vote,
                        "diseases": k.diseases,
                        "seriesinstanceuid": str(k.automatic),
                        'automatic': str(k.automatic)
                        }
                if k.automatic == 'T':
                    result_ = graphql_prediction(data, kc)
                    result_ai = graphql_Interface(data, 'result', kc)
                    result_ai['studyViewFlexible'][0]['testid'] = version + k.studyinstanceuid + str(loop)
                    update_data(result_ai['studyViewFlexible'][0])
                else:
                    graphql_prediction(data, kc)
            else:
                continue
    return True
