from TestPlatform.common.PostgreSQL import connect_postgres


def searchData(ip, time):
    data = {'studyinstanceuid': i.studyinstanceuid}
    sql = 'SELECT ----开始move时间----，-------完成move时间--------，----状态---- FROM dds的表 ORDER BY 一个attribute'
    dds_record = connect_postgres(host=ip, sql=sql)
    dds_record_data = dds_record.to_dict(orient='dict')