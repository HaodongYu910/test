# from TestPlatform.utils.graphql.get_graphql_result import get_graphql_result
from ..utils.graphql.graphql_prediction import graphql_Interface
from TestPlatform.common.regexUtil import *
from TestPlatform.models import stress_detail_record, stress_data
from django.db import transaction
from TestPlatform.serializers import stressdetail_Serializer, stressdetail_Deserializer
import time


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


def sequence(orthanc_ip, loop_time, diseases, version):
    kc = use_keycloak_bmutils(orthanc_ip, "biomind", "password")
    data = stress_data.objects.filter()
    for loop in range(int(loop_time)):
        """Execute Test sequence."""
        for k in data:
            if k.diseases in diseases:
                data = {"version": version,
                        "testid": version + k.studyinstanceuid + str(loop),
                        "patientid": k.patientid,
                        "studyinstanceuid": k.studyinstanceuid,
                        "vote":k.vote,
                        "diseases": k.diseases,
                        "automatic": str(k.automatic)
                        }
                if k.automatic == 'T':
                    result_ = graphql_prediction(data, kc)
                    update_data(data)
                else:
                    result_ = graphql_prediction(data, kc)
                    if loop == 0:
                        result_ = graphql_prediction(data, kc)
                    else:
                        ai_data = {'studyinstanceuid': version + k.studyinstanceuid + str(loop - 1)}
                        while True:
                            result_ai = graphql_Interface(ai_data, result_ai, kc)
                            if result_ai['studyViewFlexible'][0]['aistatus'] in ['-1', '0', '1', '2', '3']:
                                update_data(result_ai['studyViewFlexible'][0])
                                result_ = graphql_prediction(data, kc)
                                break
            else:
                continue
    get_tc_perf()
    return True
