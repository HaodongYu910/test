from TestPlatform.common.regexUtil import *
from TestPlatform.utils.graphql.graphql_utils import GraphQLDriver
from TestPlatform.models import stress_result
from TestPlatform.serializers import stress_result_Deserializer,stress_result_Serializer
from django.db import transaction

logger = logging.getLogger(__name__)

def selectsql(**kwargs):
    sql = {
        'prediction': "select \
                 modelname,\
                 count(predid),\
                 cast(avg(predictionsec) as decimal(8, 2)) as \"avg\",\
                 percentile_disc(0.5) within group(order by predictionsec) as \"median\",\
                 cast(min(predictionsec) as decimal(8, 2)) as \"min\",\
                 cast(max(predictionsec) as decimal(8, 2)) as \"max\",\
                 cast(stddev(predictionsec) / avg(predictionsec) as decimal(8, 2)) as \"coef\" from prediction_metrics\
            where endpredictionts between '{0}' and '{1}'\
            and modelname != 'bodypart' and  predictionsec >3\
            group by modelname\
            order by min(startpredictionts)".format(kwargs['starttime'],kwargs['endtime']),\
        'job': "select pm.modelname, \
                 count(jm.jobid) as \"count\",\
                 cast(avg(jm.jobsec) as decimal(8, 2))  as \"avg\",\
                 cast(EXTRACT(EPOCH FROM(max(jm.endjobts) - min(jm.startjobts))) / count(jm.jobid) as decimal(8, 2))  as \"single\",\
                 percentile_disc(0.5) within group(order by jm.jobsec)  as \"median\",\
                 cast(min(jm.jobsec) as decimal(8, 2)) as \"min\", \
                 cast(max(jm.jobsec) as decimal(8, 2)) as \"max\",\
                 cast(stddev(jm.jobsec) / avg(jm.jobsec) as decimal(8, 2)) as \"coef\"\
           From job_metrics jm JOIN prediction_metrics pm on jm.studyuid= pm.studyuid \
           where jm.endjobts between '{0}' and '{1}'\
                and jm.mode = 'auto'\
                group by pm.modelname\
                order by min(jm.startjobts)".format(kwargs['starttime'],kwargs['endtime']), 'job_metrics': "SELECT studyuid,\
            MIN ( receivejobts ),\
            MIN ( startjobts ),\
            MAX ( startjobts ),\
            COUNT ( jobid ),\
            AVG ( jobsec )\
        FROM job_metrics\
        WHERE receivejobts between '{0}' and '{1}'\
        GROUP BY studyuid\
        ORDER BY MIN ( receivejobts )".format(kwargs['starttime'],kwargs['endtime']),
        'lung': "select studyuid from prediction_metrics where modelname='lungct' and " \
            "startpredictionts BETWEEN '{0}' and '{1}' ".format(kwargs['starttime'],kwargs['endtime']),
        'lungch': "select {3} as slicenumber ,modelname, \
                        count(predid) as \"count\", \
                        cast(avg(predictionsec) as decimal(8,2)) as \"avg\", \
                        percentile_disc(0.5) within group (order by predictionsec) as \"median\",\
                        cast(min(predictionsec) as decimal(8,2)) as \"min\", \
                        cast(max(predictionsec) as decimal(8,2)) as \"max\",\
                        cast(stddev(predictionsec)/avg(predictionsec) as decimal(8,2)) as \"coef\" \
                        from prediction_metrics \
                        where endpredictionts BETWEEN '{0}'and'{1}'and modelname = 'lungct' \
                        and studyuid in ({2}) and  predictionsec >3 group by modelname\
                        order by min(startpredictionts);".format(kwargs['starttime'],kwargs['endtime'],kwargs['studyuid'],kwargs['slicenumber'])}.get(kwargs['sqltable'], 'error')

    return sql


def lung(checkdate,server,version):
    kc = use_keycloak_bmutils(server, "test", "Asd@123456")
    db_query =selectsql(sqltable="lung",
                        starttime=checkdate[0],
                        endtime=checkdate[1],
                        studyuid='',
                        slicenumber=''
                        )
    result_db = connect_to_postgres(server, db_query)
    result_dict = result_db.to_dict(orient='records')
    dict = {}
    for line in result_dict:
        graphql_query = '{ studies(StudyInstanceUID:"' + line["studyuid"] + '"){ HanalyticsProtocols { pseries_classifier }' \
                                                                            'Series{  SeriesInstanceUID ' \
                                                                            'Instances{ SliceThickness } } } }'
        graphql = GraphQLDriver('/graphql', kc)
        results = graphql.execute_query(graphql_query)
        if results['studies']==[]:
            continue
        elif results['studies'][0]['HanalyticsProtocols'][0]['pseries_classifier'] is None:
            continue
        else:
            for i in results['studies'][0]['Series']:
                lung = results['studies'][0]['HanalyticsProtocols'][0]['pseries_classifier']['CT_Lung']
                Series = i['SeriesInstanceUID']

                if lung.find(Series)>=0:
                    SliceThickness = round(float(i['Instances'][0]['SliceThickness']), 2)
            if dict.get(SliceThickness) is None:
                dict[SliceThickness] = '\'' + str(line["studyuid"]) + '\''
            else:
                a = dict[SliceThickness]
                dict[SliceThickness] = a + ',\'' + str(line["studyuid"]) + '\''
    for key in dict.keys():
        result_db = connect_to_postgres(server, selectsql(sqltable="lungch",
                                                          starttime=checkdate[0],
                                                          endtime=checkdate[1],
                                                          studyuid=dict[key],
                                                          slicenumber =key ))
        result_dict = result_db.to_dict(orient='records')
        for i in result_dict:
            i["version"] = version
            i["type"] = 'lung'
            stressserializer = stress_result_Deserializer(data=i)
            with transaction.atomic():
                stressserializer.is_valid()
                stressserializer.save()
    return result_dict


def dataCheck(datadict1,datadict2):
    _dict1 = stress_result_Deserializer(datadict1, many=True)
    _dict2=stress_result_Deserializer(datadict2, many=True)
    dict1=_dict1.data
    dict2 = _dict2.data
    for i in dict1:
        for j in dict2:
            if i['slicenumber'] is None:
                a = i['modelname']
                b = j['modelname']
            else:
                a = i['slicenumber']
                b = j['slicenumber']
            if a == b:
                for x in ['avg','single','median','min','max','coef','rate']:
                    if i[x] is None:i[x] = 0
                    if j[x] is None:j[x] = 0
                    if i[x] > j[x]:
                        i[x] = str(i[x]) + " （ +" + str(
                            '%.2f' % (float(i[x]) - float(j[x]))) + ")"
                    elif i[x] <j[x]:
                        i[x] = str(i[x]) + " ( " + str(
                            '%.2f' % (float(i[x]) - float(j[x]))) + ")"
    return dict1


def savecheck(sqltable, checkdate,server,version):
    result_1 = connect_to_postgres(server,selectsql(sqltable=sqltable,
                                                    starttime=checkdate[0],
                                                    endtime=checkdate[1],
                                                    studyuid='',
                                                    slicenumber=''
                                                    ))
    _num1 = len(result_1)
    _dict1 = result_1.to_dict(orient='records')
    for i in _dict1:
        i["version"]=version
        i["type"]=sqltable
        stressserializer = stress_result_Deserializer(data=i)
        with transaction.atomic():
            stressserializer.is_valid()
            stressserializer.save()
    return True
