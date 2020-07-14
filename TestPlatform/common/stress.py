# from TestPlatform.utils.graphql.get_graphql_result import get_graphql_result
from ..utils.graphql.graphql_prediction import graphql_Interface
from TestPlatform.common.regexUtil import *
from TestPlatform.models import stress_detail_record
from django.db import transaction
from TestPlatform.serializers import stressdetail_Serializer,stressdetail_Deserializer
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
        results = graphql_Interface(data, kc)
        duration = time.time() - start_time
        data['duration'] = duration
        data['report'] = str(results['ai_biomind']['preport'])
        stress_detailserializer = stressdetail_Serializer(data=data)
        with transaction.atomic():
            stress_detailserializer.is_valid()
            stress_detailserializer.save()
    except Exception as e:
        logging.error('Query failed: {0}'.format(e))
        return e
    return True


def sequence(orthanc_ip, loop_time, csvname, version):
    kc = use_keycloak_bmutils(orthanc_ip, "biomind", "password")
    for loop in range(int(loop_time)):
        ai_data={'ai':'ai'}
        """Execute Test sequence."""
        for line in getcsv(csvname):
            # get TestData from postgres database
            db_query = \
                "SELECT \"StudyInstanceUID\",\"SeriesInstanceUID\" " \
                "from \"Series\"" \
                "where \"StudyInstanceUID\" = '" + line['studyinstanceuid'] + "'" + \
                "ORDER BY \"SeriesNumber\" DESC limit 1;"
            try:
                result_db = connect_to_postgres(orthanc_ip, db_query)
                result_dict = result_db.to_dict(orient='records')
                result_num = len(result_db)
            except:
                fail_msg = "[FAILED]Failed to connect to Postgres. "
                logging.error(fail_msg)
                return False, fail_msg

            if result_num == 0:
                continue
            else:
                for k in result_dict:
                    data = {"version": version,
                            "testid": version + line['studyinstanceuid'] + str(loop),
                            "patientid": line['patientid'],
                            "studyinstanceuid": line['studyinstanceuid'],
                            "seriesinstanceuid": k['SeriesInstanceUID'],
                            "diseases": line['diseases'],
                            "automatic": str(line['automatic'])
                            }
                    if line['automatic'] == True:
                        result_ = graphql_prediction(data, kc)
                        update_data(data)
                    else:
                        result_ = graphql_prediction(data, kc)
                        # if loop == 0:
                        #     result_ = graphql_prediction(data, kc)
                        # else:
                        #     ai_data['studyinstanceuid'] = version + line['studyinstanceuid'] + str(loop - 1)
                        #     while True:
                        #         result_ai = graphql_Interface(ai_data, kc)
                        #         if result_ai['studyViewFlexible'][0]['aistatus'] in ['-1', '0', '1', '2', '3']:
                        #             update_data(result_ai['studyViewFlexible'][0])
                        #             result_ = graphql_prediction(data, kc)
                        #             break

    get_tc_perf()
    return True


