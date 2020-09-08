from TestPlatform.common.regexUtil import *
from TestPlatform.utils.graphql.graphql_utils import GraphQLDriver

def selectsql(**kwargs):
    sql = {
        'prediction': "select \
                 modelname,\
                 count(predid),\
                 cast(avg(predictionsec) as decimal(8, 2)) as \"avg_pred_time\",\
                 percentile_disc(0.5) within group(order by predictionsec) as \"median_pred_time\",\
                 cast(min(predictionsec) as decimal(8, 2)) as \"min_pred_time\",\
                 cast(max(predictionsec) as decimal(8, 2)) as \"max_pred_time\",\
                 cast(stddev(predictionsec) / avg(predictionsec) as decimal(8, 2)) as \"coef\" from prediction_metrics\
            where endpredictionts between '{0}' and '{1}'\
            and modelname != 'bodypart' and  predictionsec >3\
            group by modelname\
            order by min(startpredictionts)".format(kwargs['starttime'],kwargs['endtime']),\
        'job': "select pm.modelname, \
                 count(jm.jobid) as \"job_count\",\
                 cast(avg(jm.jobsec) as decimal(8, 2))  as \"avg_job_time\",\
                 cast(EXTRACT(EPOCH FROM(max(jm.endjobts) - min(jm.startjobts))) / count(jm.jobid) as decimal(8, 2))  as \"avg_single_job_time\",\
                 percentile_disc(0.5) within group(order by jm.jobsec)  as \"median_job_time\",\
                 cast(min(jm.jobsec) as decimal(8, 2)) as \"min_job_time\", \
                 cast(max(jm.jobsec) as decimal(8, 2)) as \"max_job_time\",\
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
        'lungch': "select modelname, \
                        count(predid) as \"job_count\", \
                        cast(avg(predictionsec) as decimal(8,2)) as \"avg_pred_time\", \
                        percentile_disc(0.5) within group (order by predictionsec) as \"median_pred_time\",\
                        cast(min(predictionsec) as decimal(8,2)) as \"min_pred_time\", \
                        cast(max(predictionsec) as decimal(8,2)) as \"max_pred_time\",\
                        cast(stddev(predictionsec)/avg(predictionsec) as decimal(8,2)) as \"coef\" \
                        from prediction_metrics \
                        where endpredictionts BETWEEN '{0}'and'{1}'and modelname = 'lungct' \
                        and studyuid in ({2}) group by modelname\
                        order by min(startpredictionts);".format(kwargs['starttime'],kwargs['endtime'],kwargs['studyuid'],kwargs['slicenumber'])}.get(kwargs['sqltable'], 'error')

    return sql


def datacheck(sqltable, checkfield, checkdate,server):
    result_1 = connect_to_postgres(server,selectsql(sqltable=sqltable,
                                                    starttime=checkdate[0][0],
                                                    endtime=checkdate[0][1],
                                                    studyuid='',
                                                    slicenumber=''
                                                    ))
    _num1 = len(result_1)
    _dict1 = result_1.to_dict(orient='records')
    result_2 = connect_to_postgres(server,selectsql(sqltable=sqltable,
                                                    starttime=checkdate[1][0],
                                                    endtime=checkdate[1][1],
                                                    studyuid='',
                                                    slicenumber=''
                                                    ))
    _dict2 = result_2.to_dict(orient='records')
    _num2 = len(result_2)

    for i in range(_num1):
        for j in range(_num2):
            if _dict1[i]['modelname'] == _dict2[j]['modelname']:
                for x in checkfield:
                    if _dict1[i][x] is None:
                        _dict1[i][x] = 0
                    if _dict2[j][x] is None:
                        _dict2[j][x] = 0
                    if _dict1[i][x] > _dict2[j][x]:
                        _dict1[i][x] = str(_dict1[i][x]) + " （ +" + str(
                            '%.2f' % (float(_dict1[i][x]) - float(_dict2[j][x]))) + ")"
                    elif _dict1[i][x] <_dict2[j][x]:
                        _dict1[i][x] = str(_dict1[i][x]) + " ( " + str(
                            '%.2f' % (float(_dict1[i][x]) - float(_dict2[j][x]))) + ")"
    return _dict1




def lung(sqltable, checkfield, checkdate,server):
    kc = use_keycloak_bmutils(server, "test", "Asd@123456")
    db_query =selectsql(sqltable="lung",
                        starttime=checkdate[0][0],
                        endtime=checkdate[0][1],
                        studyuid='',
                        slicenumber=''
                        )
    result_db = connect_to_postgres(server, db_query)
    result_dict = result_db.to_dict(orient='records')
    dict = {}
    for line in result_dict:
        graphql_query = '{ studies(StudyInstanceUID:"' + line["studyuid"] + '"){' \
                                                                            'Series{ ' \
                                                                            'Instances{ SliceThickness } } } }'
        graphql = GraphQLDriver('/graphql', kc)
        results = graphql.execute_query(graphql_query)
        if results['studies']==[]:
            continue
        else:
            SliceThickness = round(float(results['studies'][0]['Series'][0]['Instances'][0]['SliceThickness']), 2)
            if dict.get(SliceThickness) is None:
                dict[SliceThickness] = '\'' + str(line["studyuid"]) + '\''
            else:
                a = dict[SliceThickness]
                dict[SliceThickness] = a + ',\'' + str(line["studyuid"]) + '\''
    for key in dict.keys():
        result_db = connect_to_postgres(server, selectsql(sqltable="lungch",
                                                          starttime=checkdate[0][0],
                                                          endtime=checkdate[0][1],
                                                          studyuid=key,
                                                          slicenumber = dict[key]))
        result_dict = result_db.to_dict(orient='records')
    return result_dict


def dataCheck(datadict1,datadict2,check_field):
    _dict1=datadict1
    _dict2=datadict2
    checkfield=check_field
    _num1 = len(_dict1)
    _num2 = len(_dict2)

    for i in range(_num1):
        for j in range(_num2):
            if _dict1[i]['modelname'] == _dict2[j]['modelname']:
                for x in checkfield:
                    if _dict1[i][x] is None:
                        _dict1[i][x] = 0
                    if _dict2[j][x] is None:
                        _dict2[j][x] = 0
                    if _dict1[i][x] > _dict2[j][x]:
                        _dict1[i][x] = str(_dict1[i][x]) + " （ +" + str(
                            '%.2f' % (float(_dict1[i][x]) - float(_dict2[j][x]))) + ")"
                    elif _dict1[i][x] <_dict2[j][x]:
                        _dict1[i][x] = str(_dict1[i][x]) + " ( " + str(
                            '%.2f' % (float(_dict1[i][x]) - float(_dict2[j][x]))) + ")"
    return _dict1