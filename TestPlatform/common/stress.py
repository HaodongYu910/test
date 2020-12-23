# from TestPlatform.utils.graphql.get_graphql_result import get_graphql_result
from ..utils.graphql.graphql import graphql_Interface
from TestPlatform.common.regexUtil import *
from TestPlatform.models import dicom_record, dicom
from django.db import transaction
from TestPlatform.serializers import stress_Deserializer
import datetime
from django.conf import settings

logger = logging.getLogger(__name__)

# 修改数据
def update_data(data):
    obj = dicom_record.objects.get(testid=data["testid"])
    serializer = stress_Deserializer(data=data)
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
        stress_detailserializer = stress_Deserializer(data=data)
        with transaction.atomic():
            stress_detailserializer.is_valid()
            stress_detailserializer.save()
    except Exception as e:
        logger.error('Query failed: {0}'.format(e))
        return e
    return True


def sequence(orthanc_ip,end_time, diseases, version):
    kc = use_keycloak_bmutils(orthanc_ip,settings.BiomindUser, settings.Biomindpasswd)
    stressdata = dicom.objects.filter()
    loop=0
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
                    graphql_prediction(data, kc)
                    # result_ai = graphql_Interface(data, 'result', kc)
                    # result_ai['studyViewFlexible'][0]['testid'] = version + k.studyinstanceuid + str(loop)
                    # update_data(result_ai['studyViewFlexible'][0])
                else:
                    graphql_prediction(data, kc)
            else:
                continue
    return True
