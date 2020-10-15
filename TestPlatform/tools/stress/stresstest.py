# from TestPlatform.utils.graphql.get_graphql_result import get_graphql_result
import gc
from TestPlatform.utils.graphql.graphql_prediction import graphql_Interface
from TestPlatform.utils.graphql.graphql_del_hanalyticsreportt import *
from TestPlatform.common.regexUtil import *
from TestPlatform.models import stress_detail_record, stress_data
from django.db import transaction
from TestPlatform.serializers import stressdetail_Serializer, stressdetail_Deserializer
import os
import shutil
from .PerformanceResult import savecheck, lung

logger = logging.getLogger(__name__)


# 修改数据
def updateStressData(uid,orthanc_ip):
    vote = ''
    Series = connect_to_postgres(orthanc_ip,
                                 "select \"SeriesInstanceUID\" from \"Series\" where \"StudyInstanceUID\" ='{0}'".format(
                                     uid)).to_dict(orient='records')
    pseries_classifier = connect_to_postgres(orthanc_ip,
                                             "select protocol->'pseries_classifier' as \"pseries\" from hanalyticsprotocol where studyuid ='{0}' LIMIT 1;".format(
                                                 uid)).to_dict(orient='records')

    pseries = pseries_classifier[0]['pseries']
    for key in pseries:
        for i in Series:
            if str(i['SeriesInstanceUID']) in str(pseries[key]):
                vote = vote + '{0}: \\"{1}\\",'.format(str(key), str(i['SeriesInstanceUID']))
    vote = "{" + vote + "}"
    return vote
def savecsv(path,graphql_query):
    f = open('{0}'.format(path), 'a', encoding='utf-8', newline="")
    csv_writer = csv.writer(f)
    csv_writer.writerow(graphql_query)
    f.close()

def stress(orthanc_ip, diseases,version,thread,loop,synchronizing,ramp,time):
    path =os.path.join(os.getcwd())
    shutil.rmtree('{0}/stress'.format(path))
    os.mkdir(path + './stress')
    savecsv('{0}/stress/config.csv'.format(path), [orthanc_ip,'test','Asd@123456',thread,synchronizing,loop,ramp,time,version])
    # 循环生成压测数据
    for i in diseases:
        stressdata = stress_data.objects.filter(diseases=i)

        for k in stressdata:
            graphql_query = "{ ai_biomind (" \
                        "study_uid:\\\"" + str(k.studyinstanceuid) + "\\\", protocols:" \
                                                       "{ pothers: " \
                                                       "{ disable_negative_voting:false} " \
                                                       "penable_cached_results:false pconfig:{} " \
                                                       "planguage:\\\"zh-cn\\\" " \
                                                       " puser_id:\\\"biomind\\\" " \
                                                       "pseries_classifier:" + str(k.vote) + "})" \
            " { pprediction pmetadata SOPInstanceUID pconfig  pseries_classifier pstatus_code } }"
            if i=="Lung" and k.automatic =='1.25':
                savecsv('{0}/stress/{1}1.csv'.format(path, str(i)), [graphql_query])
            elif i=="Lung" and k.automatic =='1.5':
                savecsv('{0}/stress/{1}2.csv'.format(path, str(i)), [graphql_query])
            elif i=="Lung" and k.automatic =='5':
                savecsv('{0}/stress/{1}3.csv'.format(path, str(i)), [graphql_query])
            elif i=="Lung" and k.automatic =='10':
                savecsv('{0}/stress/{1}4.csv'.format(path, str(i)), [graphql_query])
            else:
                savecsv('{0}/stress/{1}.csv'.format(path,str(i)), [graphql_query])
    try:
        start_time = datetime.datetime.now().strftime("%Y-%m-%d%H:%M:%S")
        cmd = 'jmeter -n -t {0}/load.jmx -l {1}/logs/{2}.jtl -j {3}/logs/jmeter{4}.log'.format(path,path,start_time,path,start_time)
        logger.info(cmd)
        os.system(cmd)
    except Exception as e:
        logger.error("执行jmeter失败{0}".format(e))
