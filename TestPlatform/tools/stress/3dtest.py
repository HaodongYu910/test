from TestPlatform.common.regexUtil import *
import threading


def testjson():
    content = [{
        "study_id": "00cd6fc8-0d82a4e0-970dae1f-916e6c7e-6f086af2",
        "study_uid": "1.2.840.113619.2.416.126627296069071647610671185223528287450",
        "modalities": "CT",
        "language": "zh-cn"
    }, {
        "study_id": "21cefe3a-42bc3de4-c8fdc0b2-d110feba-ff4a9826",
        "study_uid": "1.2.840.113619.2.416.297723402920242770870129435910306530950",
        "modalities": "CT",
        "language": "zh-cn"
    }, {
        "study_id": "c3d69dff-0624d47a-fcceda52-50dd0b9d-08bcce11",
        "study_uid": "1.2.840.113619.2.416.190274922218387255633568974860423556001",
        "modalities": "CT",
        "language": "zh-cn"
    }, {
        "study_id": "d2581f58-a3721d32-920ac990-8998bf97-53d0cbee",
        "study_uid": "1.2.840.113619.2.416.42233201131450268962796251011403203461",
        "modalities": "CT",
        "language": "zh-cn"
    }, {
        "study_id": "a39424cb-db9e8383-fa2d7c00-63e41cff-28867a22",
        "study_uid": "1.2.840.113619.2.416.266453326091684583138340293391469751478",
        "modalities": "CT",
        "language": "zh-cn"
    }, {
        "study_id": "181e4d4a-b7c94878-f365dcee-7b2dd5f2-8f65915a",
        "study_uid": "1.3.46.670589.33.1.63685739833892714300001.5657507089302031300",
        "modalities": "CT",
        "language": "zh-cn"
    }, {
        "study_id": "f3c662f9-81bad2ea-44e3291c-11ba27c3-02e94b77",
        "study_uid": "1.2.840.113619.2.416.81290132466489141527235328124986173918",
        "modalities": "CT",
        "language": "zh-cn"
    }]
    return content


def sequence(loop_time, serverip):
    kc = use_keycloak_bmutils(serverip, "biomind", "password")
    for loop in range(int(loop_time)):
        def testkc(kc, content):
            print((content))
            # kc = use_keycloak_bmutils(self.orthanc_ip, "biomind", "password")
            r = kc.post(
                url='/3D/vessel/vesselLoadImages/',
                timeout=120,
                json=content
            )
            if r is None:
                uid = '37623e7dcba94003897a9a70a1f17068'
            else:
                content['uid'] = r.json()['uid']

            if uid:
                k = kc.post(
                    url='/3D/vessel/vesselClearImages/',
                    timeout=120,
                    verify=False,
                    json=content
                )
            return k

        for i in testjson():
            threading.Thread(target=testkc, args=(kc, i,)).start()
            time.sleep(1)
        time.sleep(2)


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