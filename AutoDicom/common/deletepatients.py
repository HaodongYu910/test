# coding=utf-8

from AutoTest.common.PostgreSQL import connect_postgres
from AutoTest.models import dictionary
from AutoTest.utils.keycloak.login_kc import *
import logging
from ..models import dicom
logger = logging.getLogger(__name__)

def delete_patients_duration(key, serverID,type,fuzzy):
    Hostobj =Server.objects.get(id=serverID)
    data = {}
    if type == 'gold':
        sqldict = dictionary.objects.get(key=type, type="sql", status=True)
        sqldata = dicom.objects.filter(type='gold')
        strsql = "'"
        for i in sqldata:
            strsql = strsql + str(i.studyinstanceuid)+"','"
        sql = sqldict.value.format(strsql[:-2])
    elif type in ["patientid","patientname","studyinstanceuid"]:
        sqldict = dictionary.objects.get(key='publicid', type="sql", status=True)
        if fuzzy is True:
            fuzzy = 'like'
            key = key + '%'
        else:
            fuzzy = '='
        sql = sqldict.value.format(type,fuzzy,key)
    else:
        sqldict = dictionary.objects.get(key=type, type="sql", status=True)
        sql = sqldict.value
    try:
        result_1 = connect_postgres(host=Hostobj.id, sql=sql, database="orthanc")
        _dict1 = result_1.to_dict(orient='records')
        kc = login_keycloak(serverID)
    except Exception as e:
        logger.error("failed to find patirents: error[{0}]".format(e))
        return False

    for oid in _dict1:
        try:
            publicid = oid["publicid"]
            kc.delete('/orthanc/studies/{0}'.format(publicid), timeout=120)
            data[oid["patientname"]]=oid["studyinstanceuid"]
        except Exception as e:
            logger.error("failed to delete patientv [{0}]: error[{1}]".format(oid, e))
            return False
    return data
