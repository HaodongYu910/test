import gc
from TestPlatform.utils.graphql.graphql_del_hanalyticsreportt import *
from TestPlatform.common.regexUtil import *
from TestPlatform.models import  stress_data

import os
import shutil

logger = logging.getLogger(__name__)



def lungSlice(server,studyuid):
    kc = use_keycloak_bmutils(server, "test", "Asd@123456")
    graphql_query = '{ studies(StudyInstanceUID:"' + studyuid + '"){ HanalyticsProtocols { pseries_classifier }' \
                                                                        'Series{  SeriesInstanceUID ' \
                                                                        'Instances{ SliceThickness } } } }'
    graphql = GraphQLDriver('/graphql', kc)
    results = graphql.execute_query(graphql_query)
    if results['studies'] == []:
        return 1
    elif results['studies'][0]['HanalyticsProtocols'][0]['pseries_classifier'] is None:
        return 1
    else:
        for i in results['studies'][0]['Series']:
            lung = results['studies'][0]['HanalyticsProtocols'][0]['pseries_classifier']['CT_Lung']
            Series = i['SeriesInstanceUID']
            if lung.find(Series) >= 0:
                SliceThickness = round(float(i['Instances'][0]['SliceThickness']), 2)

    return SliceThickness

# 修改数据
def updateStressData(uid, orthanc_ip):
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


def savecsv(path, graphql_query):
    f = open('{0}'.format(path), 'a', encoding='utf-8', newline="")
    csv_writer = csv.writer(f)
    csv_writer.writerow(graphql_query)
    f.close()


def stress(orthanc_ip, diseases, version, thread, loop, synchronizing, ramp, time):
    path = os.path.join(os.getcwd())
    if not os.path.exists('{0}/stress'.format(path)):
        os.mkdir(path + '/stress')
    else:
        shutil.rmtree('{0}/stress'.format(path))
        os.mkdir(path + '/stress')
    list=[orthanc_ip, 'test', 'Asd@123456', thread, synchronizing, ramp, time, version]
    for k in ['Brain',  'CTA', 'CTP', 'Lung', 'MRA', 'coronary', 'Heart', 'Neck', 'post_surgery','Breast']:
        a = loop if k in diseases else 0
        list.append(a)

    savecsv('{0}/stress/config.csv'.format(path),list)

    # 循环生成压测数据
    for i in diseases:
        stressdata = stress_data.objects.filter(server=orthanc_ip,diseases=i)
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
            if i == "Lung" and k.slicenumber == '1.25':
                savecsv('{0}/stress/{1}1.csv'.format(path, str(i)), [graphql_query])
            elif i == "Lung" and k.slicenumber == '1.5':
                savecsv('{0}/stress/{1}2.csv'.format(path, str(i)), [graphql_query])
            elif i == "Lung" and k.slicenumber == '5.0':
                savecsv('{0}/stress/{1}3.csv'.format(path, str(i)), [graphql_query])
            elif i == "Lung" and k.slicenumber == '10.0':
                savecsv('{0}/stress/{1}4.csv'.format(path, str(i)), [graphql_query])
            else:
                savecsv('{0}/stress/{1}.csv'.format(path, str(i)), [graphql_query])
    # 执行jmeter
    try:
        start_time = datetime.datetime.now().strftime("%Y-%m-%d%H%M%S")
        cmd = 'nohup jmeter -n -t {0}/stress.jmx -l {1}/logs/{2}.jtl -j {3}/logs/jmeter{4}.log &'.format(path, path, start_time,
                                                                                  path, start_time)
        logger.info(cmd)
        os.system(cmd)
    except Exception as e:
        logger.error("执行jmeter失败{0}".format(e))
