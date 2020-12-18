# from TestPlatform.utils.graphql.get_graphql_result import get_graphql_result
import gc

from TestPlatform.utils.graphql.graphql import graphql_Interface
from TestPlatform.common.regexUtil import *
from TestPlatform.models import dicom_record, dictionary, stress_record, stress
from django.db import transaction
from TestPlatform.serializers import dicomrecord_Deserializer, dicomrecord_Serializer
import datetime
from ..dicom.dicomdetail import Predictor
from ..dicom.dicomdetail import voteData, Slice
from .PerformanceResult import saveResult, lung

logger = logging.getLogger(__name__)


# 修改数据
def update_data(data):
    obj = dicom_record.objects.get(testid=data["testid"])
    serializer = dicomrecord_Serializer(data=data)
    with transaction.atomic():
        if serializer.is_valid():
            serializer.update(instance=obj, validated_data=data)


# 调用graphql 存储记录接口
def graphql_prediction(data, kc):
    try:
        start_time = time.time()
        results = graphql_Interface(data, kc)
        data['duration'] = time.time() - start_time
        data['report'] = str(results['ai_biomind']['preport'])
        stress_detailserializer = dicomrecord_Serializer(data=data)
        with transaction.atomic():
            stress_detailserializer.is_valid()
            stress_detailserializer.save()
    except Exception as e:
        logger.error('Query failed: {0}'.format(e))
        return e
    return True


# 删除dicom报告
def delreport(kc, studyinstanceuid):
    try:
        graphql_query = 'mutation{ ' \
                        'deleteReport( studyuid:' + str(studyinstanceuid) + ' )' \
                                                                            'deleteProtocol( studyuid:' + str(
            studyinstanceuid) + ' ) }'
        graphql_Interface(graphql_query, kc)
    except:
        logger.error("删除失败{0}".format(studyinstanceuid))


# 手动预测

def Manual(orthanc_ip, diseases, count):
    server = orthanc_ip
    start_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    kc = use_keycloak_bmutils(server, "test", "Asd@123456")
    stressdata = stress_record.objects.filter(diseases=diseases)
    info = {}
    i = 0
    for k in stressdata:
        if info.get(k.diseases):
            if i == count:
                continue
            else:
                i = i + 1
        else:
            info[k.diseases] = k.diseases
        delreport(kc, k.studyuid)
        graphql_query = '{ ' \
                        'ai_biomind(' \
                        'block : false' \
                        ' study_uid: "' + str(k.studyuid) + '"' \
                                                            ' protocols: {' \
                                                            ' penable_cached_results: false' \
                                                            ' }' \
                                                            '){' \
                                                            '  pprediction' \
                                                            '  preport' \
                                                            '  pcontour' \
                                                            '  pmodels' \
                                                            '  pstudy_uid' \
                                                            '}' \
                                                            '}'

        graphql_Interface(graphql_query, kc)
        # info[k.slicenumber] = info[k.slicenumber] + 1


# 自动预测压测循环
def AutoPrediction(orthanc_ip, diseases, count):
    server = orthanc_ip
    kc = use_keycloak_bmutils(server, "test", "Asd@123456")
    info = {}
    for i in diseases.split(","):
        stressdata = stress_record.objects.filter(diseases=i )
        for k in stressdata:
            if str(i) == '9':
                if info.get(k.slicenumber):
                    if info[k.slicenumber] == count:
                        continue
                    else:
                        info[k.slicenumber] = info[k.slicenumber] + 1
                else:
                    info[k.slicenumber] = 1
            else:
                if info.get(k.diseases):
                    if info[k.diseases] == count:
                        continue
                    else:
                        info[k.diseases] = info[k.diseases] + 1
                else:
                    info[k.diseases] = 1
            delreport(kc, k.studyuid)
            graphql_query = '{ ' \
                            'ai_biomind(' \
                            'block : false' \
                            ' study_uid: "' + str(k.studyuid) + '"' \
                                                                ' protocols: {' \
                                                                ' penable_cached_results: false' \
                                                                ' }' \
                                                                '){' \
                                                                '  pprediction' \
                                                                '  preport' \
                                                                '  pcontour' \
                                                                '  pmodels' \
                                                                '  pstudy_uid' \
                                                                '}' \
                                                                '}'

            graphql_Interface(graphql_query, kc)
            # info[k.slicenumber] = info[k.slicenumber] + 1


# 生成自动预测测试数据
def stresscache(stressid):
    obj = stress.objects.get(id=stressid)
    # 循环病种存储 测试数据
    for i in obj.testdata.split(","):
        dictobj = dictionary.objects.get(id =i)
        # 查询预测成功的数据 作为压测数据
        # sql = 'select  DISTINCT studyuid from  prediction_metrics where modelname =\'brainctp\' ORDER BY modelname';
        sql = 'select  DISTINCT studyuid from  prediction_metrics where modelname like \'%{0}%\''.format(dictobj.key)
        results = connect_to_postgres(obj.loadserver, sql).to_dict(orient='records')
        # 循环插入数据
        for j in results:
            logger.info(j['studyuid'])
            # graphql_query, imagecount, slicenumber=None,None,None
            graphql_query, imagecount, slicenumber = voteData(j['studyuid'], obj.loadserver,int(i))
            data = {"stressid": stressid,
                    "studyuid": j['studyuid'],
                    "imagecount": imagecount,
                    "slicenumber": slicenumber,
                    "diseases": i,
                    "graphql": None
                    }
            stress_record.objects.create(**data)
