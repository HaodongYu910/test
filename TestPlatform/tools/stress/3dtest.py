from TestPlatform.common.regexUtil import *
import threading


class loadtest():
    def __init__(self):
        self.loop_time = 200000
        self.kc = use_keycloak_bmutils('192.168.1.208', "test", "111111")
        self.content = [{
            "study_id": "00cd6fc8-0d82a4e0-970dae1f-916e6c7e-6f086af2",
            "study_uid": "1.2.840.113619.2.416.126627296069071647610671185223528287450",
            "modalities": "CT"
        }, {
            "study_id": "00cd6fc8-0d82a4e0-970dae1f-916e6c7e-6f086af2",
            "study_uid": "1.2.840.113619.2.416.126627296069071647610671185223528287450",
            "modalities": "CT"
        }, {
            "study_id": "21cefe3a-42bc3de4-c8fdc0b2-d110feba-ff4a9826",
            "study_uid": "1.2.840.113619.2.416.297723402920242770870129435910306530950",
            "modalities": "CT"
        }, {
            "study_id": "a39424cb-db9e8383-fa2d7c00-63e41cff-28867a22",
            "study_uid": "1.2.840.113619.2.416.266453326091684583138340293391469751478",
            "modalities": "CT"
        }, {
            "study_id": "f3c662f9-81bad2ea-44e3291c-11ba27c3-02e94b77",
            "study_uid": "1.2.840.113619.2.416.81290132466489141527235328124986173918",
            "modalities": "CT"
        }]

    def sequence(self):
        for loop in range(int(self.loop_time)):
            def testkc(kc, content):
                print((content))
                # kc = use_keycloak_bmutils(self.orthanc_ip, "biomind", "password")
                r = kc.post(
                    url='/3D/vessel/vesselLoadImages/',
                    timeout=120,
                    json=content
                )
                if r is None:
                    uid='37623e7dcba94003897a9a70a1f17068'
                else:
                    uid = r.json()['uid']

                if uid:
                    k = kc.post(
                        url='/3D/vessel/vesselClearImages/',
                        timeout=120,
                        verify=False,
                        json={"uid": uid}
                    )
                return k

            for i in self.content:
                threading.Thread(target=testkc, args=(self.kc, i,)).start()
                time.sleep(1)
                # testkc(self.kc, i)
            time.sleep(10)

if __name__ == '__main__':
    loadtest().sequence()
