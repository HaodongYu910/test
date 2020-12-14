from TestPlatform.common.regexUtil import *
from TestPlatform.utils.graphql.graphql_utils import GraphQLDriver
from TestPlatform.models import stress_result,stress_record,dictionary
from TestPlatform.serializers import stress_result_Deserializer, stress_result_Serializer
from django.db import transaction
from ..dicom.dicomdetail import voteData
import numpy as np

logger = logging.getLogger(__name__)

# 肺炎结果记录
def lung(checkdate, server, version):
    dict = {}
    imagescount ={}
    list =[]
    sql = dictionary.objects.get(key="predictionuid",type="sql")
    db_query =sql.value.format('lungct_v2',checkdate[0], checkdate[1])

    result_db = connect_to_postgres(server, db_query).to_dict(orient='records')
    for u in result_db:
        vote, imagecount, SliceThickness = voteData(u["studyuid"], server, 'lungct_v2')
        if SliceThickness is None:
            continue
        if dict.get(SliceThickness) is None:
            dict[SliceThickness] = '\'' + str(u["studyuid"]) + '\''
            imagescount[SliceThickness] =''
        else:
            dict[SliceThickness] = dict[SliceThickness] + ',\'' + str(u["studyuid"]) + '\''
            if imagecount is None:
                imagescount[SliceThickness] = imagescount[SliceThickness]
            else:
                imagescount[SliceThickness] =imagescount[SliceThickness]+','+str(int(imagecount))
    for ikey in dict.keys():
        predictionsql = dictionary.objects.get(key="lungprediction",type='sql')
        sql_prediction = predictionsql.value.format(checkdate[0],checkdate[1],dict[ikey], ikey)
        jobsql = dictionary.objects.get(key="lungjob",type='sql')
        sql_job = jobsql.value.format(checkdate[0], checkdate[1],dict[ikey],ikey)

        resultsave(server, sql_prediction, version, 'lung_prediction',imagescount[ikey])
        resultsave(server, sql_job, version, 'lung_job',imagescount[ikey])



# 数据比较检查
def dataCheck(dataA, dataB):
    dictA = stress_result_Deserializer(dataA, many=True).data
    dictB = stress_result_Deserializer(dataB, many=True).data
    for i in dictA:
        for j in dictB:
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
            else:
                continue
    return dictA

# 保存lung 等结果 'lung_prediction'
def resultsave(server, sql, version, type , image):
    result = connect_to_postgres(server, sql).to_dict(orient='records')
    imagelist =[]
    for j in image[1:].split(","):
        imagelist.append(int(j))
    for i in result:
        i["version"] = version
        i["type"] = type
        i["avgimages"], i["maximages"], i["minimages"] = str('%.2f' % np.mean(imagelist)),str(np.max(imagelist)),str(np.min(imagelist))
        stressserializer = stress_result_Deserializer(data=i)
        with transaction.atomic():
            stressserializer.is_valid()
            stressserializer.save()

# 预测数据保存
def savecheck(sqltable, checkdate, server, version):
    sql =dictionary.objects.get(key=sqltable,type='sql')
    selectsql=sql.value.format(checkdate[0],checkdate[1])
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
    if modelname in ['brainctp']:
        sql=dictionary.objects.get(key='predictionuid',type='sql')
        sqldata=sql.value.format(modelname,checkdate[0],checkdate[1])
        result = connect_to_postgres(server,sqldata )
        dict = result.to_dict(orient='records')
        for i in dict:
            vote,imagecount,slicenumber=voteData(i['studyuid'],server,modelname)
            if imagecount is None:
                continue
            else:
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
