# coding=utf-8
from ...common.regexUtil import *


def delete_patients_duration(key, server_ip):
    kc = use_keycloak_bmutils(server_ip, 'biomind', 'password')
    try:
        res = kc.get('/orthanc/patients', timeout=300, verify=False)
        orthanc_ids = eval(res.content)
    except Exception as e:
        logging.error("failed to find patirents: error[{0}]".format(e))
        return False,e

    for oid in orthanc_ids:
        try:
            res = kc.get('/orthanc/patients/{0}'.format(oid), timeout=120, verify=False)
            pinfo = json.loads(res.content)
        except Exception as e:
            logging.error("failed to get patient info [{0}]: error[{1}]".format(oid, e))
            continue
        pid = pinfo.get("MainDicomTags", {}).get("PatientID", "")
        if pid.find(key) >= 0:
            try:
                kc.delete('/orthanc/patients/{0}'.format(oid), timeout=120)
            except Exception as e:
                logging.error("failed to delete patientv [{0}]: error[{1}]".format(oid, e))
                return False, e
