import logging
from .graphql_utils import GraphQLDriver


def graphql_Interface(data, kc):
    if data['automatic'] == 'False':
        graphql_query = '{ ' \
                        'ai_biomind(' \
                        'block : false' \
                        ' study_uid: "' + str(data['studyinstanceuid']) + '"' \
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
    elif data['automatic'] == 'True':
        graphql_query = '{ ' \
                        'ai_biomind(' \
                        ' study_uid: "' + str(data['studyinstanceuid']) + '"' \
                                                                          ' protocols: { pconfig: {} ' \
                                                                          ' penable_cached_results: false ' \
                                                                          ' planguage: "zh-cn"' \
                                                                          ' puser_id:"biomind"' \
                                                                          ' pseries_classifier: {' \
                        + data['diseases'] + ': "' + data['seriesinstanceuid'] + '"}})' \
                                                                                 '{' \
                                                                                 '  pprediction' \
                                                                                 '  preport' \
                                                                                 '  pmodels' \
                                                                                 '  pcontour' \
                                                                                 '  pstudy_uid' \
                                                                                 '}' \
                                                                                 '}'
    elif data['ai']=='ai':
        graphql_query = '{ ' \
                        'studyView(filter:[{filter:studyinstanceuid,value:[ "' + str(data['studyinstanceuid']) + '"' \
                                                                                                              '],type: FuzzyMatch,category: PatientInfo}])' \
                                                                                                              '{' \
                                                                                                              ' aistatus' \
                                                                                                              ' diagnosis' \
                                                                                                              ' starttime' \
                                                                                                              ' completiontime' \
                                                                                                              '}' \
                                                                                                              '}'
    try:
        graphql = GraphQLDriver('/graphql', kc)
        results = graphql.execute_query(graphql_query)
    except Exception as e:
        logging.error('Query failed: {0}'.format(e))
    return results
