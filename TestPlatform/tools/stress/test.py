from TestPlatform.common.regexUtil import *
import threading


def graphql_json():
    content = {
        "study_id": "00cd6fc8-0d82a4e0-970dae1f-916e6c7e-6f086af2",
        "study_uid": "1.2.840.113619.2.416.126627296069071647610671185223528287450",
        "modalities": "CT",
        "language": "zh-cn"
    }
    return content


def sequence(serverip,studyuid):
    try:
        kc = KeycloakClient('https://{}'.format(serverip), 'test', 'Asd@123456')
        kc.login("biomind", "password")
        return kc
    except Exception as e:
        logger.error('Query failed: {0}'.format(e))
        return e
    for uid in studyuid:
        graphql_query = graphql_json(uid)
        try:
            graphql = GraphQLDriver('/graphql', kc)
            logger.info(graphql)
            results = graphql.execute_query(graphql_query)
            logger.info(results)
        except Exception as e:
            logger.error('Query failed: {0}'.format(e))


if __name__ == '__main__':
    sequence("192.168.1.124")

# sequence(10, '192.168.1.208')


# def testusr():
#     kc = use_keycloak_bmutils('192.168.1.32', "biomind", "password")
#     for loop in range(int(10)):
#         content={"username": "test"+str(loop),
#                  "group_id": "44be0473-c073-4c55-b780-bf784820ee5f",
#                  "password": "Asd@123456",
#                   "confirm": "Asd@123456",
#                  "firstname": "测",
#                  "lastname":"试"+str(loop)}
#         r = kc.post(
#             url='/annotation/user/keycloak/create/',
#             timeout=120,
#             json=content
#         )
# testusr()