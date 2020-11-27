import logging
from .graphql_utils import GraphQLDriver

logger = logging.getLogger(__name__)


def graphql_json(data):
    if data['slicenumber'] == 'F':
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
    else:
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

    return graphql_query


def graphql_Interface(graphql_query, kc):
    try:
        graphql = GraphQLDriver('/graphql', kc)
        logger.info(graphql)
        results = graphql.execute_query(graphql_query)
        logger.info(results)
        return results
    except Exception as e:
        logger.error('Query failed: {0}'.format(e))
