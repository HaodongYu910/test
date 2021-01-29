from TestPlatform.common.regexUtil import *
from TestPlatform.utils.graphql.graphql_utils import GraphQLDriver
from TestPlatform.models import stress_job,stress_record,dictionary
from TestPlatform.serializers import stress_result_Deserializer, stress_result_Serializer
from django.db import transaction
from ..dicom.dicomdetail import voteData
import numpy as np
import time

logger = logging.getLogger(__name__)

# 肺炎结果记录
def lung(checkdate, server, version,lungid,kc):
    dict = {}
    imagescount ={}
    # 查询sql
    dise = dictionary.objects.get(id=lungid)
    sql = dictionary.objects.get(key="predictionuid",type="sql")
    # db_query = 'select studyinstanceuid from study_view where aistatus =\'3\''
    db_query =sql.value.format(dise.key,checkdate[0], checkdate[1])

    result_db = connect_to_postgres(server, db_query).to_dict(orient='records')
    for u in result_db:
        vote, imagecount, SliceThickness = voteData(u["studyuid"], server,int(lungid),kc)
        if SliceThickness is None:
            continue
        if dict.get(SliceThickness) is None:
            dict[SliceThickness] = '\'' + str(u["studyuid"]) + '\''
            imagescount[SliceThickness] = imagecount
        else:
            dict[SliceThickness] = dict[SliceThickness] + ',\'' + str(u["studyuid"]) + '\''
            if imagecount is None:
                imagescount[SliceThickness] = imagescount[SliceThickness]
            else:
                imagescount[SliceThickness] =imagescount[SliceThickness]+','+str(int(imagecount))
    for ikey in dict.keys():
        for j in ['lung_job']:
            sql = dictionary.objects.get(key=str(j), type='sql')
            strsql = sql.value.format(checkdate[0], checkdate[1], dict[ikey], ikey)
            saveResult(server, version,j, checkdate,strsql,imagescount[ikey],kc)

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
                try:
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
                except Exception as e:
                    logger.error("error:{0}".format(e))
                    continue

            else:
                continue
        obj = dictionary.objects.get(id=i['modelname'])
        i['modelname'] = obj.key
    return dictA


# 预测数据保存
def saveResult(server,version,type,checkdate,sql,imagedata,kc):
    imagelist = []
    result = connect_to_postgres(server,sql)
    dict = result.to_dict(orient='records')
    for i in dict:
        if type =='lung_job':
            obj = dictionary.objects.get(remarks=i["modelname"])
        elif type =="job":
            obj = dictionary.objects.get(value=i["modelname"])
        else:
            obj = dictionary.objects.get(key=i["modelname"])
        i["version"] = version
        i["type"] = type
        i["modelname"] = obj.id
        if imagedata !=[]:
            for j in imagedata[1:].split(","):
                imagelist.append(int(j))
            i["avgimages"], i["maximages"], i["minimages"] = str('%.2f' % np.mean(imagelist)), str(
                np.max(imagelist)), str(np.min(imagelist))
        else:
            i["avgimages"], i["maximages"], i["minimages"] = image(server,int(obj.id),checkdate,kc)
        stressserializer = stress_result_Deserializer(data=i)
        with transaction.atomic():
            stressserializer.is_valid()
            stressserializer.save()
    return True

# 保存 job 结果数据
def jobsaveResult(id,server,version,checkdate,kc):
    # 查询测试时间 job 数据
    images = None
    slicenumber = None
    dictobj=dictionary.objects.get(key="job_ls")
    obj = dictionary.objects.get(key="modelname")
    sql = dictobj.value.format(checkdate[0],checkdate[1])
    result = connect_to_postgres(server, sql)
    dict = result.to_dict(orient='records')
    # 循环数据保存
    for i in dict:
        try:
            sql = obj.value.format(i["studyuid"])
            result = connect_to_postgres(server, sql)
            modelname = result.to_dict(orient='records')[0]["modelname"]
            dx = dictionary.objects.get(key=modelname)
            # lung 等数据获取张数和 层厚
            if dx.id in [4, 5, 7, 8, 10, 9, 12]:
                vote, images, slicenumber = voteData(i["studyuid"], server, int(dx.id), kc)
            data ={
                "studyuid": i["studyuid"],
                "job_id": i["job_id"],
                "start": str(i["startjobts"])[:19],
                "end": str(i["endjobts"])[:19],
                "sec": str(i["sec"]),
                "modelname":dx.id,
                "version":version,
                "type":'job',
                "stressid":id,
                "images":images,
                "slicenumber":slicenumber
            }
            stress_job.objects.create(**data)
        except Exception as e:
            continue

# 求预测影像 平均值 最大值  最小值
def image(server,modelname,checkdate,kc):
    datalist=[]
    if modelname in [4,5,7,8,10]:
        obj = dictionary.objects.get(id=modelname)
        sql = dictionary.objects.get(key='predictionuid',type='sql')
        sqldata=sql.value.format(obj.key,checkdate[0],checkdate[1])
        dict = connect_to_postgres(server,sqldata ).to_dict(orient='records')
        for i in dict:
            vote,imagecount,slicenumber=voteData(i['studyuid'],server,modelname,kc)
            if imagecount is None:
                continue
            else:
                datalist.append(int(imagecount))
        try:
            return str('%.2f' % np.mean(datalist)),str(np.max(datalist)),str(np.min(datalist))
        except Exception as e:
            logger.error(e)
            return None,None,None
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


