from TestPlatform.common.regexUtil import *

def graphql_pred_influx(orthanc_ip,bodypart,study_uid,patient_id,accession_number,
                        script,vol,ai_result,duration,msg):
    cur_time = get_current_time("%Y-%m-%d %H:%M:%S", 8)
    tags = {'orthanc_ip': orthanc_ip, 'body_part': bodypart,
            'study_uid': study_uid, 'patient_id': patient_id,
            'accession_num': accession_number, 'script': script}
    fields = {'disease_volume': float(vol), 'ai_result': str(ai_result),
              'graphql_duration': float(duration), 'log_msg': msg}

    point = {"measurement": 'GraphqlResult', "time": cur_time, "fields": fields, "tags": tags}
    connect_to_influx('influx', 'influx', 'jenkins_data', 'insert', [point])
    logging.info(point)