# from TestPlatform.utils.graphql.get_graphql_result import get_graphql_result
import gc

from TestPlatform.utils.graphql.graphql import graphql_Interface
from TestPlatform.common.regexUtil import *
from TestPlatform.models import dicom_record, dicom
from django.db import transaction
from TestPlatform.serializers import dicomrecord_Deserializer, dicomrecord_Serializer
import datetime
from .PerformanceResult import savecheck,lung

logger = logging.getLogger(__name__)

# 修改数据
def update_data(data):
    obj = dicom_record.objects.get(testid=data["testid"])
    serializer = dicomrecord_Serializer(data=data)
    with transaction.atomic():
        if serializer.is_valid():
            serializer.update(instance=obj, validated_data=data)


#调用graphql 存储记录接口
def graphql_prediction(data, kc):
    try:
        start_time = time.time()
        results = graphql_Interface(data, kc)
        data['duration'] = time.time() - start_time
        data['report'] = str(results['ai_biomind']['preport'])
        stress_detailserializer = dicomrecord_Serializer(data=data)
        with transaction.atomic():
            stress_detailserializer.is_valid()
            stress_detailserializer.save()
    except Exception as e:
        logger.error('Query failed: {0}'.format(e))
        return e
    return True

# 压测循环
def sequence(orthanc_ip,end_time, diseases, version):
    server=orthanc_ip
    version=version
    start_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    kc = use_keycloak_bmutils(server, "test", "Asd@123456")
    stressdata = dicom.objects.filter(diseases__in=diseases)

    for k in stressdata:

        graphql_query = '{ ' \
                                    'ai_biomind(' \
                                'block : false' \
                                ' study_uid: "' + str(k.studyinstanceuid) + '"' \
                                                                                  ' protocols: {' \
                                                                                  ' penable_cached_results: false' \
                                                                                  ' }' \
                                                                                  '){' \
                                                                                  '  pprediction' \
                                                                                  '  preport' \
                                                                                  '  pcontour' \
                                                                                  '  pmodels' \
                                                                                  '  pstudy_uid' \
                                                                                  '}' \
                                                                                  '}'

        graphql_Interface(graphql_query, kc)

    # try:
    #     checkdate = [start_time, end_time]
    #     savecheck('job', checkdate,server,version)
    #     savecheck('prediction', checkdate,server,version)
    #     lung(checkdate, server, version)
    # except Exception as e:
    #     logger.error("生成版本测试结果失败error{0}".format(e))

