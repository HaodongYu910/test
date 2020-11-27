import gc
from TestPlatform.utils.graphql.graphql import *
from TestPlatform.common.regexUtil import *
from TestPlatform.models import dicom
from ...utils.graphql.graphql import *
from ..dicom.SendDicom import Send

import os, time
import shutil

logger = logging.getLogger(__name__)


def dicomsavecsv(ids):
    path = os.path.join(os.getcwd())
    for i in ids:
        obj = dicom.objects.get(id=i)
        graphql_query = "{ ai_biomind (" \
                        "study_uid:\\\"" + str(obj.studyinstanceuid) + "\\\", protocols:" \
                                                                       "{ pothers: " \
                                                                       "{ disable_negative_voting:false} " \
                                                                       "penable_cached_results:false pconfig:{} " \
                                                                       "planguage:\\\"zh-cn\\\" " \
                                                                       " puser_id:\\\"biomind\\\" " \
                                                                       "pseries_classifier:" + str(obj.vote) + "}" \
                                                                                                               "routes: [[\\\"generate_series\\\",\\\"series_classifier\\\",\\\"" + str(
            obj.predictor) + "\\\"]])" \
                             " { pprediction pmetadata SOPInstanceUID pconfig  pseries_classifier pstatus_code } }"
        if obj.diseases == "Lung":
            diseases = str("{0}_{1}_slicenumber".format(obj.diseases, str(obj.slicenumber)))
        else:
            diseases = obj.diseases
        savecsv(str('{0}/logs/gold.csv'.format(path)), [graphql_query, diseases, obj.diagnosis])


def goldSmoke(version,server_ip,ids):
    kc = use_keycloak_bmutils(server_ip, 'test', 'Asd@123456')
    # 循环测试数据
    for i in ids:
        try:
            obj = dicom.objects.get(id=i)
            sql ='select studyinstanceuid from study_view where studyinstanceuid = \'{0}\''.format(
                                                obj.studyinstanceuid)
            result_db = connect_to_postgres(server_ip,sql)

            if len(result_db) != 1:
                send= Send(server_ip,i,'')(server_ip,)
            graphql_query = "{ ai_biomind (" \
                            "study_uid:\\\"" + str(obj.studyinstanceuid) + "\\\", protocols:" \
                                                                           "{ pothers: " \
                                                                           "{ disable_negative_voting:false} " \
                                                                           "penable_cached_results:false pconfig:{} " \
                                                                           "planguage:\\\"zh-cn\\\" " \
                                                                           " puser_id:\\\"biomind\\\" " \
                                                                           "pseries_classifier:" + str(obj.vote) + "}" \
                                                                                                                   "routes: [[\\\"generate_series\\\",\\\"series_classifier\\\",\\\"" + str(
                obj.predictor) + "\\\"]])" \
                                 " { pprediction pmetadata SOPInstanceUID pconfig  pseries_classifier pstatus_code } }"
            start_time = datetime.datetime.now().strftime("%Y-%m-%d%H%M%S")
            result = graphql_Interface(graphql_query, kc)
            end_time = datetime.datetime.now().strftime("%Y-%m-%d%H%M%S")
        except:
            continue
        # 比对结果
        try:
            logger.info(result)
        except Exception as e:
            logger.error("比对失败{0}".format(result))


def delreport(server_ip, ids):
    kc = use_keycloak_bmutils(server_ip, 'test', 'Asd@123456')
    # 循环删除数据报告
    for i in ids:
        try:
            obj = dicom.objects.get(id=i)
            graphql_query = 'mutation{ ' \
                            'deleteReport( studyuid:' + str(obj.studyinstanceuid) + ' )' \
                                                                                    'deleteProtocol( studyuid:' + str(
                obj.studyinstanceuid) + ' ) }'
            graphql_Interface(graphql_query, kc)
        except:
            logger.error("删除失败{0}".format(obj.studyinstanceuid))
            continue
