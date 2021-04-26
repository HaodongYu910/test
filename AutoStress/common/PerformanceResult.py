from AutoProject.common.PostgreSQL import connect_postgres
from AutoProject.models import dictionary
from AutoStress.models import stress_result
from ..serializers import stress_result_Deserializer
from django.db import transaction
from AutoDicom.common.dicomBase import voteData
import numpy as np
import logging

logger = logging.getLogger(__name__)


# 肺炎结果记录
def lung(checkdate, server, version, lungid, kc):
    dict = {}
    imagescount = {}
    # 查询sql
    dise = dictionary.objects.get(id=lungid)
    sql = dictionary.objects.get(key="predictionuid", type="sql")
    # db_query = 'select studyinstanceuid as studyuid  from study_view where aistatus =\'3\''
    db_query = sql.value.format(dise.key, checkdate[0], checkdate[1])

    result_db = connect_postgres(host=server, sql=db_query, database="orthanc").to_dict(orient='records')
    for u in result_db:
        vote, imagecount, SliceThickness = voteData(u["studyuid"], server, int(lungid), kc)
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
                imagescount[SliceThickness] = imagescount[SliceThickness] + ',' + str(int(imagecount))
    for ikey in dict.keys():
        for j in ['lung_job']:
            sql = dictionary.objects.get(key=str(j), type='sql')
            strsql = sql.value.format(checkdate[0], checkdate[1], dict[ikey], ikey)
            saveResult(server, version, j, checkdate, strsql, imagescount[ikey], kc)


# 数据比较检查
def CheckData(version, stressType):
    # 按版本 查询 性能测试记录
    dictA = stress_result_Deserializer(
        stress_result.objects.filter(version=version, type=stressType[1]), many=True).data
    dictB = stress_result_Deserializer(
        stress_result.objects.filter(version=version, type=stressType[0]), many=True).data
    # 比较 性能测试记录 结果
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
                    for x in ['avg', 'single', 'median', 'min', 'max', 'coef', 'rate', 'minimages', 'maximages',
                              'avgimages']:
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


def modelData(modeldata, version, Type):
    try:
        if modeldata["slicenumber"] is None:
            predOjb = stress_result.objects.get(version=version, type=Type, modelname=modeldata["modelname"])
        else:
            predOjb = stress_result.objects.get(version=version, type=Type, modelname=modeldata["modelname"],
                                                slicenumber=modeldata["slicenumber"])
        modeldata["predavg"] = predOjb.avg
        modeldata["predsingle"] = predOjb.single
        modeldata["predmedian"] = predOjb.median
        modeldata["predmin"] = predOjb.min
        modeldata["predmax"] = predOjb.max
        modeldata["predcoef"] = predOjb.coef

        # try:
        #     modeldata["diffavg"] = float(predOjb.avg) - float(modeldata["avg"])
        # except Exception as e:
        #     modeldata["diffavg"] = 0
        # try:
        #     modeldata["diffsingle"] = float(predOjb.single) - float(modeldata["single"])
        # except Exception as e:
        #     modeldata["diffsingle"] = 0
        # try:
        #     modeldata["diffmedian"] = float(predOjb.median) - float(modeldata["median"])
        # except Exception as e:
        #     modeldata["diffmedian"] = 0
        # try:
        #     modeldata["diffmin"] = float(predOjb.min) - float(modeldata["min"])
        # except Exception as e:
        #     modeldata["diffmin"] = 0
        # try:
        #     modeldata["diffmax"] = float(predOjb.avg) - float(modeldata["max"])
        # except Exception as e:
        #     modeldata["diffmax"] = 0

    except Exception as e:
        logger.error(e)
        modeldata["predavg"] = 0
        modeldata["predsingle"] = 0
        modeldata["predmedian"] = 0
        modeldata["predmin"] = 0
        modeldata["predmax"] = 0
        modeldata["predcoef"] = 0
    return modeldata

# 数据比较检查
def dataCheck(stressType, versions):

    # 按版本 查询 性能测试记录
    dictA = stress_result_Deserializer(
        stress_result.objects.filter(version=versions[0], type=stressType[0]), many=True).data
    dictB = stress_result_Deserializer(
        stress_result.objects.filter(version=versions[1], type=stressType[0]), many=True).data
    # 比较 性能测试记录 结果
    for i in dictA:
        i = modelData(i, versions[0], stressType[1])
        for j in dictB:
            j = modelData(j, versions[1], stressType[1])

            if i['slicenumber'] is None:
                a = i['modelname']
                b = j['modelname']
            else:
                a = i['slicenumber']
                b = j['slicenumber']
            if a == b:
                try:
                    for x in ['avg', 'single', 'median', 'min', 'max', 'coef', 'rate', 'minimages', 'maximages',
                              'avgimages', 'predavg', 'predsingle', 'predmedian', 'predmin', 'predmax', 'predcoef']:
                        if i[x] is None : i[x] = 0.0
                        if j[x] is None : j[x] = 0.0

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
def saveResult(server, version, type, checkdate, sql, imagedata, kc):
    imagelist = []
    result = connect_postgres(host=server, sql=sql, database="orthanc")
    dict = result.to_dict(orient='records')
    for i in dict:
        if type == 'lung_job':
            obj = dictionary.objects.get(remarks=i["modelname"])
        elif type == "job":
            obj = dictionary.objects.get(value=i["modelname"])
        else:
            obj = dictionary.objects.get(key=i["modelname"])
        i["version"] = version
        i["type"] = type
        i["modelname"] = obj.id
        if imagedata != []:
            for j in imagedata[1:].split(","):
                imagelist.append(int(j))
            i["avgimages"], i["maximages"], i["minimages"] = str('%.2f' % np.mean(imagelist)), str(
                np.max(imagelist)), str(np.min(imagelist))
        else:
            i["avgimages"], i["maximages"], i["minimages"] = image(server, int(obj.id), checkdate, kc)
        stressserializer = stress_result_Deserializer(data=i)
        with transaction.atomic():
            stressserializer.is_valid()
            stressserializer.save()
    return True


# 求预测影像 平均值 最大值  最小值
def image(server, modelname, checkdate, kc):
    datalist = []
    if modelname in [4, 5, 7, 8, 10]:
        obj = dictionary.objects.get(id=modelname)
        sql = dictionary.objects.get(key='predictionuid', type='sql')
        sqldata = sql.value.format(obj.key, checkdate[0], checkdate[1])
        dict = connect_postgres(database="orthanc", host=server, sql=sqldata).to_dict(orient='records')
        for i in dict:
            vote, imagecount, slicenumber = voteData(i['studyuid'], server, modelname, kc)
            if imagecount is None:
                continue
            else:
                datalist.append(int(imagecount))
        try:
            return str('%.2f' % np.mean(datalist)), str(np.max(datalist)), str(np.min(datalist))
        except Exception as e:
            logger.error(e)
            return None, None, None
    else:
        return None, None, None

#
# def jmetersave(server, version):
#     task_content = ""
#     result = connect_influx('192.168.1.120', 'Jmeter_DB', 'query', task_content)
#     _num1 = len(result)
#     _dict1 = result.to_dict(orient='records')
#     for i in _dict1:
#         print(i)
#         # i["version"]=version
#         # i["type"]=sqltable
#         # stressserializer = stress_result_Deserializer(data=i)
#         # with transaction.atomic():
#         #     stressserializer.is_valid()
#         #     stressserializer.save()
#     return True
