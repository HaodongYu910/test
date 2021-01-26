# coding=utf-8

from ...common.regexUtil import *
from ...models import dicom,GlobalHost
from ...utils.keycloak.login_kc import *
import logging
logger = logging.getLogger(__name__)

def delete_patients_duration(key, serverID,type,fuzzy):
    Hostobj =GlobalHost.objects.get(id=serverID)

    if fuzzy is True:
        fuzzy='like'
        key = key+'%'
    else:
        fuzzy ='='
    data={}
    if type =='error':
        sql = "select publicid FROM \"study\"  where \"studyinstanceuid\" in (select \"studyinstanceuid\" FROM \"study\"  GROUP BY \"studyinstanceuid\" HAVING count(\"studyinstanceuid\")>1)"
    elif type =='gold':
        sqldata =dicom.objects.filter(type='gold')
        strsql ="'"
        for i in sqldata:
            strsql = strsql + str(i.studyinstanceuid)+"','"
        sql = "select publicid FROM \"Study\"  where \"StudyInstanceUID\" in ({0})".format(strsql[:-2])
    else:
        sql="select r.publicid from resources r join \"Study\" s on r.publicid = s.publicid  where s.\"{0}\" {1} '{2}'".format(type,fuzzy,key)
    try:
        result_1 = connect_to_postgres(Hostobj.host,sql)
        _dict1 = result_1.to_dict(orient='records')
        kc = login_keycloak(serverID)
    except Exception as e:
        logger.error("failed to find patirents: error[{0}]".format(e))
        return False

    for oid in _dict1:
        try:
            publicid=oid["publicid"]
            kc.delete('/orthanc/studies/{0}'.format(publicid), timeout=120)
        except Exception as e:
            logger.error("failed to delete patientv [{0}]: error[{1}]".format(oid, e))
            return False
    return _dict1