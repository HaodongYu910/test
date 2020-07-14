from TestPlatform.common.regexUtil import *


# from common.PostgreSql import *


def sql(sqltable, selectdate):
    k = {'prediction': "select studyuid,\
                 modelname,\
                 min(startpredictionts) as \"first_pred\",\
                 max(startpredictionts) as \"last_pred\",\
                 count(predid),\
                 cast(avg(predictionsec) as decimal(8, 2)) as \"avg pred time /s\",\
                 percentile_disc(0.5) within group(order by predictionsec) as \"median pred time /s\",\
                 cast(min(predictionsec) as decimal(8, 2)) as \"min pred time /s\",\
                 cast(max(predictionsec) as decimal(8, 2)) as \"max pred time /s\",\
                 cast(stddev(predictionsec) / avg(predictionsec) as decimal(8, 2)) as \"coef. of variation\" from prediction_metrics\
            where endpredictionts between '{0}' and '{1}'\
            and modelname != 'bodypart'\
            group by studyuid,modelname\
            order by min(startpredictionts)".format(selectdate[0], selectdate[1]), 'job': "select studyuid, \
                 min(startjobts) as \"first_pred\",\
                 max(startjobts) as \"last_pred\", \
                 count(jobid) as \"job_count\",\
                 cast(avg(jobsec) as decimal(8, 2))  as \"avg job time /s\",\
                 cast(EXTRACT(EPOCH FROM(max(endjobts) - min(startjobts))) / count(jobid) as decimal(8, 2))  as \"avg single job time /s\",\
                 percentile_disc(0.5)\
                 within group(order by jobsec)  as \"median job time /s\",\
                 cast(min(jobsec) as decimal(8, 2)) as \"min job time /s\", \
                 cast(max(jobsec) as decimal(8, 2)) as \"max job time /s\",\
                 cast(stddev(jobsec) / avg(jobsec) as decimal(8, 2)) as \"coef. of variation\"\
           From job_metrics\
           where endjobts between '{0}' and '{1}'\
                and mode = 'auto'\
                group by studyuid\
                order by min(startjobts)".format(selectdate[0], selectdate[1]), 'job_metrics': "SELECT studyuid,\
            MIN ( receivejobts ),\
            MIN ( startjobts ),\
            MAX ( startjobts ),\
            COUNT ( jobid ),\
            AVG ( jobsec )\
        FROM job_metrics\
        WHERE receivejobts between '{0}' and '{1}'\
        GROUP BY studyuid\
        ORDER BY MIN ( receivejobts )".format(selectdate[0], selectdate[1])}.get(sqltable, 'error')
    return k


def datacheck(sqltable, checkfield, checkdate):
    result_1 = connect_to_postgres('192.168.1.208',sql(sqltable, checkdate[0]))
    _num1 = len(result_1)
    _dict1 = result_1.to_dict(orient='records')
    print(_dict1)
    result_2 = connect_to_postgres('192.168.1.208',sql(sqltable, checkdate[1]))
    _dict2 = result_2.to_dict(orient='records')
    _num2 = len(result_2)

    for i in range(_num1):
        for j in range(_num2):
            if _dict1[i]['studyuid'] == _dict2[j]['studyuid']:
                for x in checkfield:
                    if _dict1[i][x] is None:
                        _dict1[i][x] = 0
                    if _dict2[j][x] is None:
                        _dict2[j][x] = 0
                    print(_dict1[i][x])
                    if _dict1[i][x] > _dict2[j][x]:
                        _dict1[i][x] = str(_dict1[i][x]) + "H （ +" + str(
                            '%.2f' % (float(_dict1[i][x]) - float(_dict2[j][x]))) + ")"
                    else:
                        _dict1[i][x] = str(_dict1[i][x]) + "L ( " + str(
                            '%.2f' % (float(_dict1[i][x]) - float(_dict2[j][x]))) + ")"
    return _dict1


def savedata(table, checkfield, field, checkdate, csvname):
    blist = [field]
    data = datacheck(table, checkfield, checkdate)
    for i in data:
        alist = []
        for j in field:
            a = i[j]
            alist.append(a)
        blist.append(alist)
    savecsv(blist, csvname)


def testcheck(sdate):
    savedata('prediction',
             ['avg pred time /s', 'median pred time /s', 'min pred time /s', 'max pred time /s', 'coef. of variation'],
             ['studyuid', 'modelname', 'first_pred', 'last_pred', 'count', 'avg pred time /s', 'median pred time /s',
              'min pred time /s', 'max pred time /s',
              'coef. of variation'], sdate, 'result.csv')
    savedata('job',
             ['avg job time /s', 'avg single job time /s', 'median job time /s', 'min job time /s', 'max job time /s',
              'coef. of variation'],
             ['studyuid', 'first_pred', 'last_pred', 'job_count', 'avg job time /s', "avg single job time /s",
              'median job time /s', 'min job time /s', 'max job time /s', 'coef. of variation'
              ], sdate, 'results.csv')


if __name__ == '__main__':
    list = [["2020-07-12 00:00:00", "2020-07-12 23:00:00"], ["2020-07-10 20:00:00", "2020-07-11 16:59:00"]]
    testcheck(list)
