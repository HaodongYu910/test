# from TestPlatform.utils.graphql.get_graphql_result import get_graphql_result
import gc
from TestPlatform.utils.graphql.graphql_prediction import graphql_Interface
from TestPlatform.utils.graphql.graphql_del_hanalyticsreportt import *
from TestPlatform.common.regexUtil import *
from TestPlatform.models import stress_detail_record, stress_data
from django.db import transaction
from TestPlatform.serializers import stressdetail_Serializer, stressdetail_Deserializer

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

def stress(orthanc_ip, diseases,version,thread,loop,synchronizing):
    path =os.path.join(os.getcwd())
    version = version
    f = open('{0}/stress/config.csv'.format(path), 'w', encoding='utf-8', newline="")
    csv_writer = csv.writer(f)
    # 构建列表头
    csv_writer.writerow(['sever','username','password','thread','synchronizing',
                         'loop'])
    csv_writer.writerow([orthanc_ip,'test','Asd@123456',thread,synchronizing,loop])
    # 循环生成压测数据
    for i in diseases:
        stressdata = stress_data.objects.filter(diseases=i)
        f = open('{0}/stress/{1}.csv'.format(path,str(i)), 'w', encoding='utf-8', newline="")
        # 基于文件对象构建 csv写入对象
        csv_writer = csv.writer(f)
        # 构建列表头
        csv_writer.writerow([i, "", ''])
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
            csv_writer.writerow([graphql_query, ""])
            # 5. 关闭文件
        f.close()
    try:
        start_time = datetime.datetime.now().strftime("%Y-%m-%d%H:%M:%S")
        cmd = 'jmeter -n -t {0}/stress/centos.jmx -l {1}/logs/{2}.jtl'.format(path,path,start_time)
        logger.info(cmd)
        os.system(cmd)
    except Exception as e:
        logger.error("执行jmeter失败{0}".format(e))
