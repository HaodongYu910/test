from pip._internal.utils import logging

from AutoProject.common.PostgreSQL import *
from ..models import duration_record

def dataVerify(ip,relation_id):
    UIDsql = getStudyUIDsql(relation_id)
    logger.info("find uid in testplatform success")
    verify_list = searchDataInDDS(UIDsql,ip)
    a = 0
    for i in verify_list:
        if i["imagecount"]:
            a = a + 1
    print(a)
    print("success")


def getStudyUIDsql(id):
    """
    input
        id: relation_id corresponding to the number of duration
    output
        str: a sql string combined by Study UID which are collected from Test Platform table "duration_record"
    """
    # get studyUID from duration_record table, where relation_id is same as we required
    temp_record = duration_record.objects.filter(relation_id=id)
    str = ""
    for i in range(len(temp_record)-1):
        str = str + " studyinstanceuid = " + "\'" + temp_record[i].studyinstanceuid + "\'" + " or "
    str = str + " studyinstanceuid = " + "\'" + temp_record[len(temp_record)-1].studyinstanceuid + "\'"
    # logging.info('found study in testplatform success, count: [{0}]'.format(len(temp_record)))
    return str


def searchDataInDDS(UIDsql,ip):
    """
    input:
        UIDsql: getStudyUIDsql返回值，通过查找测试平台的发送数据，将其uid拼接为一个字符串。
        ip: dds server ip
    output:
        dic_aft: an full dic with all data which has been stored in dds table
    """
    try:
        # 查询dds表格的sql语句
        sql = 'select  studyinstanceuid , insertiontime , status , imagecount FROM study where {0}'.format(UIDsql)
        # dds_record = connect_postgres_dicommaster(host=ip, sql=sql)
        dds_record = connect_postgres(host=ip, sql=sql, database="orthanc")
        temp_dic = dds_record.to_dict(orient='records')
    except Exception as e:
        # logging.info("there is no record for data {0} in dds table".format(studyuid))
        print("has error {0}".format(e))
    return temp_dic

