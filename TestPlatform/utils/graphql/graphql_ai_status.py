import logging
from TestPlatform.utils.graphql.graphql_query_kc import graphql_query_kc

def graphql_ai_status(study_uid, query_type,kc):
    ai_status_query = '{ ' \
                      'studyView(filter:[{filter:studyinstanceuid,value:[ "' + str(study_uid) + '"' \
                      '],type:ExactMatch}])'\
                      '{' \
                      ' studyinstanceuid' \
                      ' aistatus' \
                      '}' \
                      '}'
                      
    # Execute the query
    try:
        ai_status_result = graphql_query_kc(ai_status_query, query_type,kc)
    except Exception as e:
        logging.info(ai_status_query)
        logging.info('Query failed: {0}'.format(e))
        logging.error('Query failed: {0}'.format(e))
        ai_status_result = e
    return ai_status_result

