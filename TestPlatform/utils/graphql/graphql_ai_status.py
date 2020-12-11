import logging
from TestPlatform.utils.graphql.graphql_query_kc import graphql_query_kc
logger = logging.getLogger(__name__)

def graphql_ai_status(study_uid,kc):
    ai_status_query = '{ ' \
                      'studyView(filter:[{filter:studyinstanceuid,value:[ "' + str(study_uid) + '"' \
                      '],type:ExactMatch}])'\
                      '{' \
                      ' diagnosis' \
                      ' aistatus' \
                      ' starttime' \
                      ' completiontime' \
                       '}' \
                      '}'
                      
    # Execute the query
    try:
        ai_status_result = graphql_query_kc(ai_status_query,'ai',kc)
    except Exception as e:
        logger.error('Query failed: {0}'.format(e))
        ai_status_result = False
    return ai_status_result




# graphql_query = '{ ' \
#                         'studyViewFlexible(filter:[{filter:studyinstanceuid,value:[ "' + str(data['studyinstanceuid']) + '"' \
#                                                                                                                  '],type: FuzzyMatch,category: PatientInfo}])' \
#                                                                                                                  '{' \
#                                                                                                                  ' aistatus' \
#                                                                                                                  ' diagnosis' \
#                                                                                                                  ' starttime' \
#                                                                                                                  ' completiontime' \
#                                                                                                                  '}' \
#                                                                                                                  '}'
