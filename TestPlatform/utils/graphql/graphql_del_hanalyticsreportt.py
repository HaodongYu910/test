import logging
from .graphql_utils import GraphQLDriver

logger = logging.getLogger(__name__)



def graphql_delreport(data, kc):
    graphql_query =  'mutation{ '\
            'deleteReport( studyuid:' +str(data['studyinstanceuid'])+' )' \
            'deleteProtocol( studyuid:' +str(data['studyinstanceuid'])+' ) }'
    try:
        graphql = GraphQLDriver('/graphql', kc)
        graphql.execute_query(graphql_query)
    except Exception as e:
        logger.error('del failed: {0}'.format(e))

