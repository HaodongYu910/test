# coding=utf-8

from ...common.regexUtil import *
from django.conf import settings
import logging
logger = logging.getLogger(__name__)

def delete_patients_duration(key, server_ip,type,fuzzy):
    kc = use_keycloak_bmutils(server_ip,'test', 'Asd@123456')
    try:
        res = kc.get('/orthanc/patients', timeout=300, verify=False)
        orthanc_ids = eval(res.content)
    except Exception as e:
        logger.error("failed to find patirents: error[{0}]".format(e))
        return False,e


    for oid in orthanc_ids:
        try:
            res = kc.get('/orthanc/patients/{0}'.format(oid), timeout=120, verify=False)
            pinfo = json.loads(res.content)
        except Exception as e:
            logger.error("failed to get patient info [{0}]: error[{1}]".format(oid, e))
            continue
        pid = pinfo.get("MainDicomTags", {}).get("PatientID", "")
        if pid.find(key) >= 0:
            try:
                logger.info(pinfo.get("MainDicomTags", {}).get("PatientID", ""))
                kc.delete('/orthanc/patients/{0}'.format(oid), timeout=120)

            except Exception as e:
                logger.error("failed to delete patientv [{0}]: error[{1}]".format(oid, e))
                return False, e
