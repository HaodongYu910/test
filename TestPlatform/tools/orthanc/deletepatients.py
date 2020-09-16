# coding=utf-8

from ...common.regexUtil import *
import logging
logger = logging.getLogger(__name__)

def delete_patients_duration(key, server_ip,type,fuzzy):
    if fuzzy is False:
        fuzzy='like'
        key = key+'%'
    else:
        fuzzy ='='
    data={}
    sql="select r.publicid from resources r join \"Study\" s on r.publicid = s.publicid  where s.\"{0}\" {1} '{2}'".format(type,fuzzy,key)


    try:
        result_1 = connect_to_postgres(server_ip,sql)
        _num1 = len(result_1)
        _dict1 = result_1.to_dict(orient='records')
        kc = use_keycloak_bmutils(server_ip, 'test', 'Asd@123456')
    except Exception as e:
        logger.error("failed to find patirents: error[{0}]".format(e))
        return False,e


    for oid in _dict1:
        try:
            publicid=oid["publicid"]
            kc.delete('/orthanc/patients/{0}'.format(publicid), timeout=120)
        except Exception as e:
            logger.error("failed to delete patientv [{0}]: error[{1}]".format(oid, e))
            return False, e
    return data