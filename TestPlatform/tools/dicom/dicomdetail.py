import gc
from TestPlatform.utils.graphql.graphql import *
from TestPlatform.common.regexUtil import *
from TestPlatform.models import  dicom

import os,time
import shutil

logger = logging.getLogger(__name__)


def Slice(server,Seriesuid):
    kc = use_keycloak_bmutils(server, "test", "Asd@123456")
    graphql_query='{ series(SeriesInstanceUID:"' + Seriesuid + '"){ '\
        'NumberOfSeriesRelatedInstances Instances{ SliceThickness } } }'
    graphql = GraphQLDriver('/graphql', kc)
    results = graphql.execute_query(graphql_query)
    if results['series'] == []:
        return False
    elif results['series'][0]['Instances'][0] is None:
        return False
    else:
        imagecount= results['series'][0]['NumberOfSeriesRelatedInstances']
        SliceThickness = round(float(results['series'][0]['Instances'][0]['SliceThickness']), 2)

    return imagecount,SliceThickness

# 修改数据
def voteData(uid,orthanc_ip,diseases):
    vote = ''
    try:
        Series = connect_to_postgres(orthanc_ip,
                                     "select \"SeriesInstanceUID\" from \"Series\" where \"StudyInstanceUID\" ='{0}'".format(
                                         uid)).to_dict(orient='records')
        pseries_classifier = connect_to_postgres(orthanc_ip,
                                                 "select protocol->'pseries_classifier' as \"pseries\" from hanalyticsprotocol where studyuid ='{0}' LIMIT 1;".format(
                                                     uid)).to_dict(orient='records')

        pseries = pseries_classifier[0]['pseries']
    except Exception as e:
        logger.info("没有此数据信息{0}".format(e))
        return None,None,None

    for key in pseries:
        for i in Series:
            if str(i['SeriesInstanceUID']) in str(pseries[key]):
                vote = vote + '{0}: \"{1}\",'.format(str(key), str(i['SeriesInstanceUID']))
                SeriesInstanceUID=str(i['SeriesInstanceUID'])
    vote = "{"+vote+"}"
    try:
        if diseases in ['Lung', 'CTA', 'CTP', 'coronary']:
            imagecount, slicenumber, = Slice(orthanc_ip, SeriesInstanceUID)
        else:
            imagecount, slicenumber =None,None
    except Exception as e:
        return None,None,None
    return str(vote),imagecount,slicenumber

def Predictor(diseases):
    if diseases == 'Lung':
        predictor = 'lungct_predictor'
    elif diseases in ['Brain', 'SVD', 'SWI', 'Tumor', 'post_surgery']:
        predictor = 'brainmri_predictor'
    elif diseases == 'Breast':
        predictor = 'breastmri_predictor'
    elif diseases == 'coronary':
        predictor = 'corocta_predictor'
    elif diseases == 'CTA':
        predictor = 'braincta_predictor'
    elif diseases == 'CTP':
        predictor = 'brainctp_predictor'
    elif diseases == 'Hematoma':
        predictor = 'brainct_predictor'
    elif diseases == 'Heart':
        predictor = 'heartmri_predictor'
    elif diseases == 'Neck':
        predictor = 'archcta_predictor'
    elif diseases == 'MRA':
        predictor = 'brainctp_predictor'
    else:
        predictor = None
    return predictor
def delFolder(folder):
    if os.path.exists(folder):
        shutil.rmtree(folder)
    # # 循环生成压测数据
    # for i in diseases:
    #     stressdata = dicom.objects.filter(server=orthanc_ip,diseases=i)
    #     for k in stressdata:
    #         graphql_query = "{ ai_biomind (" \
    #                         "study_uid:\\\"" + str(k.studyinstanceuid) + "\\\", protocols:" \
    #                                                                      "{ pothers: " \
    #                                                                      "{ disable_negative_voting:false} " \
    #                                                                      "penable_cached_results:false pconfig:{} " \
    #                                                                      "planguage:\\\"zh-cn\\\" " \
    #                                                                      " puser_id:\\\"biomind\\\" " \
    #                                                                      "pseries_classifier:" + str(k.vote) + "}" \
    #                                                                                                            "routes: [[\\\"generate_series\\\",\\\"series_classifier\\\",\\\""+ str(k.predictor) +"\\\"]])" \
    #                                                                                                          " { pprediction pmetadata SOPInstanceUID pconfig  pseries_classifier pstatus_code } }"
    # 
    #         if i == "Lung":
    #             dis = str("{0}_{1}_slicenumber".format(i,str(k.slicenumber)))
    #         else:
    #             dis = i
           
            # if i == "Lung" and k.slicenumber == '1.25':
            #     savecsv('{0}/stress/{1}1.csv'.format(path, str(i)), [graphql_query])
            # elif i == "Lung" and k.slicenumber == '1.5':
            #     savecsv('{0}/stress/{1}2.csv'.format(path, str(i)), [graphql_query])
            # elif i == "Lung" and k.slicenumber == '5.0':
            #     savecsv('{0}/stress/{1}3.csv'.format(path, str(i)), [graphql_query])
            # elif i == "Lung" and k.slicenumber == '10.0':
            #     savecsv('{0}/stress/{1}4.csv'.format(path, str(i)), [graphql_query])
            # else:
