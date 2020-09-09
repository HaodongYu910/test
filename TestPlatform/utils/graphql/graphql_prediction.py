import logging
from .graphql_utils import GraphQLDriver


def graphql_json(data, type):
    if type == 'ai' and data['automatic'] == 'F':
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
    elif type == 'ai' and data['automatic'] == 'T':
        graphql_query = '{ ' \
                        'ai_biomind(' \
                        ' study_uid: "' + str(data['studyinstanceuid']) + '"' \
                                                                          ' protocols: { pconfig: {} ' \
                                                                          ' penable_cached_results: false ' \
                                                                          ' planguage: "zh-cn"' \
                                                                          ' puser_id:"biomind"' \
                                                                          ' pseries_classifier: ' + data['vote'] + '})' \
                                          '{' \
                                          '  pprediction' \
                                          '  preport' \
                                          '  pmodels' \
                                          '  pcontour' \
                                          '  pstudy_uid' \
                                          '}' \
                                          '}'
    elif type == 'result':
        graphql_query = '{ ' \
                        'studyViewFlexible(filter:[{filter:studyinstanceuid,value:[ "' + str(data['studyinstanceuid']) + '"' \
                                                                                                                 '],type: FuzzyMatch,category: PatientInfo}])' \
                                                                                                                 '{' \
                                                                                                                 ' aistatus' \
                                                                                                                 ' diagnosis' \
                                                                                                                 ' starttime' \
                                                                                                                 ' completiontime' \
                                                                                                                 '}' \
                                                                                                                 '}'
    return graphql_query


def graphql_Interface(data, type, kc):
    graphql_query = graphql_json(data, type)
    try:
        graphql = GraphQLDriver('/graphql', kc)
        results = graphql.execute_query(graphql_query)
    except Exception as e:
        logger.error('Query failed: {0}'.format(e))
    return results
