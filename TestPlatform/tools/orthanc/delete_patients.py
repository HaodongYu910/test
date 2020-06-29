# coding=utf-8

import os
import sys
import json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UTILS_DIR = os.path.join(BASE_DIR, "utils")
sys.path.append(UTILS_DIR)

from TestPlatform.utils.keycloak.keycloakclient import KeycloakClient

class DeletePatients():
    def __init__(self):
        self.kc = KeycloakClient('https://{0}:{1}'.format(
            '124.193.253.120', '8443'), 'biomind',
            'password')
        self.kc.login('biomind', 'password')

    def delete_patients_duration(self):
        key_words = "duration"
        try:
            res = self.kc.get('/orthanc/patients', timeout=60, verify=False)
            orthanc_ids = eval(res.content)
        except Exception as e:
            print ("failed to find patirents: error[{0}]".format(e))
            return False

        for oid in orthanc_ids:
            try:
                res = self.kc.get('/orthanc/patients/{0}'.format(oid), timeout=60, verify=False)
                pinfo = json.loads(res.content)
            except Exception as e:
                print ("failed to get patient info [{0}]: error[{1}]".format(oid, e))
                continue

            pid = pinfo.get("MainDicomTags", {}).get("PatientID", "")
            if pid.find(key_words) >= 0:
                try:
                    self.kc.delete('/orthanc/patients/{0}'.format(oid), timeout=60)
                except Exception as e:
                    print ("failed to delete patientv [{0}]: error[{1}]".format(oid, e))


if __name__ == "__main__":
    dp = DeletePatients()
    dp.delete_patients_duration()