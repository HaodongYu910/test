from TestPlatform.utils.graphql.graphql_utils import GraphQLDriver

def graphql_query_kc(content, query_type,kc):
    if query_type == 'graphql':
        try:
            graphql = GraphQLDriver('/graphql', kc)
            results = graphql.execute_query(content)
            return results
        except:
            print('Autotest.')
            return 'Graphql query error or timeout.'
    elif query_type == 'get':
        try:
            results = kc.get(content, verify=False)
            return results.json()
        except:
            print('Get query error or timeout.')
            return 'Get query error or timeout.'
    else:
        pass