import logging
from .graphql_utils import GraphQLDriver

logger = logging.getLogger(__name__)


def graphql_Interface(graphql_query, kc):
    try:
        graphql = GraphQLDriver('/graphql', kc)
        logger.info("graphql_query : {}".format(graphql_query))
        results = graphql.execute_query(graphql_query)
        logger.info("results : {}".format(results))
        return results
    except Exception as e:
        logger.error('failed: {0},results {1}'.format(e, results))
        return e

