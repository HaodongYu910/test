from TestPlatform.common.regexUtil import *
from TestPlatform.utils.graphql.graphql_utils import GraphQLDriver
from TestPlatform.models import stress_result,stress_record,interface
from TestPlatform.serializers import stress_result_Deserializer, stress_result_Serializer
from django.db import transaction
from ..dicom.dicomdetail import voteData
import numpy as np

logger = logging.getLogger(__name__)

# 肺炎结果记录
def lung(checkdate, server, version):
    dict = {}
    count ={}
    list =[]
    sql = interface.objects.get(interfacename="predictionuid",type="sql")
    db_query =sql.json.format('lung',checkdate[0], checkdate[1])

    result_db = connect_to_postgres(server, db_query).to_dict(orient='records')
    for u in result_db:
        vote, imagecount, SliceThickness = voteData(u["studyuid"], server, 'Lung')
        if dict.get(SliceThickness) is None:
            dict[SliceThickness] = '\'' + str(u["studyuid"]) + '\''
        else:
            a = dict[SliceThickness]
            dict[SliceThickness] = a + ',\'' + str(u["studyuid"]) + '\''
            count[SliceThickness] =list.append(imagecount)
    for key in dict.keys():
        predictionsql = interface.objects.get(interface="lungprediction",type='sql')
        sql_prediction = predictionsql.json.format(checkdate[0],checkdate[1],dict[key], key)
        jobsql = interface.objects.get(interface="lungjob",type='sql')
        sql_job = jobsql.json.format(checkdate[0], checkdate[1],dict[key],key)

        resultsave(server, sql_prediction, version, 'lung_prediction')
        resultsave(server, sql_job, version, 'lung_job')


# def lung(checkdate, server, version):
#     di =""
#     obj = stress_record.objects.filter(slicenumber='10.0')
#     for i in obj:
#
#         di =di+ ',\'' + str(i.studyuid) + '\''
#     di =di[1:]
#     sql_prediction = "select {3} as slicenumber ,modelname, \
#                         count(predid) as \"count\", \
#                         cast(avg(predictionsec) as decimal(8,2)) as \"avg\", \
#                         percentile_disc(0.5) within group (order by predictionsec) as \"median\",\
#                         cast(min(predictionsec) as decimal(8,2)) as \"min\", \
#                         cast(max(predictionsec) as decimal(8,2)) as \"max\",\
#                         cast(stddev(predictionsec)/avg(predictionsec) as decimal(8,2)) as \"coef\" \
#                         from prediction_metrics \
#                         where endpredictionts BETWEEN '{0}'and'{1}'and modelname like '%lung%' \
#                         and studyuid in ({2}) and  predictionsec >3 group by modelname\
#                         order by min(startpredictionts);".format(checkdate[0],checkdate[1],
#                                                                  di, '10.0')
#     sql_job = "select {3} as slicenumber,pm.modelname,\
#                      count(jm.job_id) as \"count\",\
#                      cast(avg(jm.jobsec) as decimal(8, 2))  as \"avg\",\
#                      cast(EXTRACT(EPOCH FROM(max(jm.endjobts) - min(jm.startjobts))) / count(jm.job_id) as decimal(8, 2))  as \"single\",\
#                      percentile_disc(0.5) within group(order by jm.jobsec)  as \"median\",\
#                      cast(min(jm.jobsec) as decimal(8, 2)) as \"min\", \
#                      cast(max(jm.jobsec) as decimal(8, 2)) as \"max\",\
#                      cast(stddev(jm.jobsec) / avg(jm.jobsec) as decimal(8, 2)) as \"coef\"\
#                From job_metrics jm JOIN prediction_metrics pm on jm.studyuid= pm.studyuid \
#                where jm.endjobts between '{0}' and '{1}'\
#                     and jm.mode = 'auto'\
#                     and jm.studyuid in ({2}) and pm.modelname != 'bodypart'\
#                     group by pm.modelname\
#                     order by min(jm.startjobts)".format(checkdate[0], checkdate[1],di,'10.0')
#
#     resultsave(server, sql_prediction, version, 'lung_prediction')
#     resultsave(server, sql_job, version, 'lung_job')

# 保存lung 等结果 'lung_prediction'
def resultsave(server, sql, version, type):
    result = connect_to_postgres(server, sql).to_dict(orient='records')
    for i in result:
        i["version"] = version
        i["type"] = type
        stressserializer = stress_result_Deserializer(data=i)
        with transaction.atomic():
            stressserializer.is_valid()
            stressserializer.save()

# 数据比较检查
def dataCheck(datadict1, datadict2):
    _dict1 = stress_result_Deserializer(datadict1, many=True)
    _dict2 = stress_result_Deserializer(datadict2, many=True)
    dict1 = _dict1.data
    dict2 = _dict2.data
    for i in dict1:
        print(i)
        for j in dict2:
            if i['slicenumber'] is None:
                a = i['modelname']
                b = j['modelname']
            else:
                a = i['slicenumber']
                b = j['slicenumber']
            if a == b:
                for x in ['avg', 'single', 'median', 'min', 'max', 'coef', 'rate','minimages','maximages','avgimages']:
                    if i[x] is None: i[x] = 0.0
                    if j[x] is None: j[x] = 0.0
                    if float(i[x]) > float(j[x]):
                        i[x] = str(i[x]) + "(+" + str(
                            '%.2f' % (float(i[x]) - float(j[x]))) + ")"
                    elif float(i[x]) == float(j[x]):
                        i[x] = str(i[x])
                    else:
                        i[x] = str(i[x]) + " (" + str(
                            '%.2f' % (float(i[x]) - float(j[x]))) + ")"
    return dict1

# 预测数据保存
def savecheck(sqltable, checkdate, server, version):
    sql =interface.objects.get(interfacename=sqltable,type='sql')
    selectsql=sql.json.format(checkdate[0],checkdate[1])
    result = connect_to_postgres(server,selectsql)
    _num1 = len(result)
    dict = result.to_dict(orient='records')
    for i in dict:
        i["version"] = version
        i["type"] = sqltable
        i["avgimages"], i["maximages"], i["minimages"] = image(server,i['modelname'],checkdate)
        stressserializer = stress_result_Deserializer(data=i)
        with transaction.atomic():
            stressserializer.is_valid()
            stressserializer.save()
    return True

# 求预测影像 平均值 最大值  最小值
def image(server,modelname,checkdate):
    datalist=[]
    if modelname in ['brainctp', 'corocta', 'archcta', 'headcta','lungct_v2']:
        sql=interface.objects.get(interfacename='predictionuid',type='sql')
        sqldata=sql.json.format(modelname,checkdate[0],checkdate[1])
        result = connect_to_postgres(server,sqldata )
        dict = result.to_dict(orient='records')
        for i in dict:
            vote,imagecount,slicenumber=voteData(i['studyuid'],server,modelname)
            datalist.append(int(imagecount))

        return str('%.2f' % np.mean(datalist)),str(np.max(datalist)),str(np.min(datalist))
    else:
        return None,None,None

def jmetersave(server, version):
    task_content = ""
    result = connect_to_influx('192.168.2.38', 'Jmeter_DB', 'query', task_content)
    _num1 = len(result)
    _dict1 = result.to_dict(orient='records')
    for i in _dict1:
        print(i)
        # i["version"]=version
        # i["type"]=sqltable
        # stressserializer = stress_result_Deserializer(data=i)
        # with transaction.atomic():
        #     stressserializer.is_valid()
        #     stressserializer.save()
    return True
