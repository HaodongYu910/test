import logging, time
from TestPlatform.utils.graphql.graphql_query_kc import graphql_query_kc


def graphql_prediction(study_uid, query_type, need_result, kc):
    if need_result == "false":
        graphql_query = '{ ' \
                        'ai_biomind(' \
                        'block : false' \
                        ' study_uid: "' + str(study_uid) + '"' \
                                                           'protocols: {' \
                                                           'penable_cached_results: False' \
                                                           '}' \
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
                        ' study_uid: "' + str(study_uid) + '"' \
                                                           '){' \
                                                           '  pprediction' \
                                                           '  preport' \
                                                           '  pmodels' \
                                                           '  pcontour' \
                                                           '  pstudy_uid' \
                                                           '}' \
                                                           '}'

        # Execute the query
    start_time = time.time()
    try:
        queryresult = graphql_query_kc(graphql_query, query_type, kc)
    except Exception as e:
        logging.info('Query failed: {0}'.format(e))
        logging.error('Query failed: {0}'.format(e))
        queryresult = e
    duration = time.time() - start_time
    return queryresult, duration
