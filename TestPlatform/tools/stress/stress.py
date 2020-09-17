# from TestPlatform.utils.graphql.get_graphql_result import get_graphql_result
from TestPlatform.utils.graphql.graphql_prediction import graphql_Interface
from TestPlatform.utils.graphql.graphql_del_hanalyticsreportt import *
from TestPlatform.common.regexUtil import *
from TestPlatform.models import stress_detail_record, stress_data
from django.db import transaction
from TestPlatform.serializers import stressdetail_Serializer, stressdetail_Deserializer
import datetime
from .PerformanceResult import savecheck,lung

logger = logging.getLogger(__name__)

# 修改数据
def update_data(data):
    obj = stress_detail_record.objects.get(testid=data["testid"])
    serializer = stressdetail_Deserializer(data=data)
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
        stress_detailserializer = stressdetail_Serializer(data=data)
        with transaction.atomic():
            stress_detailserializer.is_valid()
            stress_detailserializer.save()
    except Exception as e:
        logger.error('Query failed: {0}'.format(e))
        return e
    return True



def stress(stressdata,diseases,kc):
    for k in stressdata:
        if k.diseases in diseases:
            data = {
                    "studyinstanceuid": k.studyinstanceuid,
                    "vote": k.vote,
                    "diseases": k.diseases,
                    "seriesinstanceuid": str(k.automatic),
                    'automatic': str(k.automatic)
                    }
            graphql_delreport(data, kc)
            graphql_Interface(data, kc)
        else:
            continue
# 压测循环
def sequence(orthanc_ip,end_time, diseases, version):
    server=orthanc_ip
    version=version
    start_time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    kc = use_keycloak_bmutils(server, "test", "Asd@123456")
    stressdata = stress_data.objects.filter()
    loop=0
    while datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") <= end_time:
        """Execute Test sequence."""
        if loop==0:
            for k in stressdata:
                if k.diseases in diseases:
                    data = {
                        "studyinstanceuid": k.studyinstanceuid,
                        "vote": k.vote,
                        "diseases": k.diseases,
                        "seriesinstanceuid": str(k.automatic),
                        'automatic': str(k.automatic)
                    }
                    graphql_delreport(data, kc)
                    graphql_Interface(data, kc)
                else:
                    continue
        else:
            for k in stressdata:
                if k.diseases in diseases:
                    data = {
                        "studyinstanceuid": k.studyinstanceuid,
                        "vote": k.vote,
                        "diseases": k.diseases,
                        "seriesinstanceuid": str(k.automatic),
                        'automatic': str(k.automatic)
                    }
                    db = connect_to_postgres(server, "select studyuid from hanalyticsreport where studyuid ='"+k.studyinstanceuid+"'")
                    _dict1 = db.to_dict(orient='records')
                    graphql_delreport(data, kc)
                    graphql_Interface(data, kc)
                else:
                    continue

        #loop = loop + 1
    checkdate=[start_time,end_time]
    savecheck('job', checkdate,server,version)
    savecheck('prediction', checkdate,server,version)
    lung(checkdate, server, version)
