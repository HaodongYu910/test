import logging,time
from AutoTest.utils.graphql.graphql_query_kc import graphql_query_kc
logger = logging.getLogger(__name__)

def graphql_prediction_series(study_uid, series_classifier, query_type, need_result,kc):

    if need_result == "false":
        graphql_query = '{ ' \
                      'ai_biomind(' \
                      'block:false' \
                      ' study_uid: "' + str(study_uid) + '"' \
                      ' protocols:{' \
                      ' pseries_classifier:{' + str(series_classifier) + '"' \
                      '}}){' \
                      ' pclassification' \
                      ' pprediction' \
                      ' preport' \
                      ' pcontour' \
                      ' pmodels' \
                      ' pstudy_uid' \
                      '}' \
                      '}'
    else:
        graphql_query = '{ ' \
                      'ai_biomind(' \
                      ' study_uid: "' + str(study_uid) + '"' \
                      ' protocols:{' \
                      ' pseries_classifier:{' + str(series_classifier) + \
                      '}}){' \
                      ' pclassification' \
                      ' pprediction' \
                      ' preport' \
                      ' pcontour' \
                      ' pmodels' \
                      ' pstudy_uid' \
                      '}' \
                      '}'

    # Execute the query
    start_time = time.time()
    logger.info(graphql_query)
    try:
        queryresult = graphql_query_kc(graphql_query, query_type,kc)
    except Exception as e:
        logger.error('Query failed: {0}'.format(e))
        queryresult = e
    duration = time.time() - start_time
    return queryresult, duration