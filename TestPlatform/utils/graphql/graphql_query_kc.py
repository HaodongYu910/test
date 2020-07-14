from TestPlatform.utils.graphql.graphql_utils import GraphQLDriver

def graphql_query_kc(content, query_type,kc):
    if query_type == 'post':
        try:
            results = kc.post(content, verify=False)
            return results.json()
        except:
            return 'Post query error or timeout.'
    elif query_type == 'get':
        try:
            results = kc.get(content, verify=False)
            return results.json()
        except:
            return 'Get query error or timeout.'
    else:
        try:
            graphql = GraphQLDriver('/graphql', kc)
            results = graphql.execute_query(content)
            return results
        except:
            return 'Graphql query error or timeout.'