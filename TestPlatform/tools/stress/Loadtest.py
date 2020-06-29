from TestPlatform.utils.graphql.get_graphql_result import get_graphql_result
from TestPlatform.utils.graphql.graphql_prediction import graphql_prediction
from TestPlatform.utils.graphql.graphql_pred_influx import graphql_pred_influx
from TestPlatform.common.regexUtil import *

class loadtest():
    def __init__(self):
        self.loop_time = 1
        self.query_number = 1  # no of TestData u want to get from
    def sequence(self):
        """Execute Test sequence."""
        for line in getcsv(csvname):
            uid = line['studyinstanceuid']
            print("-----------------")
            print(uid)
            # get TestData from postgres database
            db_query = \
                "SELECT distinct studyinstanceuid " \
                "from study_view " \
                "where studyinstanceuid = '" + uid + "'" +\
                "limit " + str(self.query_number) + \
                ";"
            try:
                result_db = connect_to_postgres(db_query)
                logging.info(result_db)
                result_num = len(result_db)
                logging.info(result_num)
            except:
                fail_msg = "[FAILED]Failed to connect to Postgres. "
                logging.error(fail_msg)
                return False

            if result_num > 0:

                kc = use_keycloak_bmutils(orthanc_ip, "biomind", "password")
                for loop in range(int(self.loop_time)):
                    result_dict = result_db.to_dict(orient='records')
                    for line in result_dict:
                        study_uid = line['studyinstanceuid']
                        logging.info('study_uid: {}'.format(study_uid))
                        if need_result == 'true':
                            logging.info("block:true")
                            patient_id = line['patientid']
                            accession_number = line['accessionnumber']
                            script = 'GenerateGraphqlPostgres'
                            cat, vol, ai_result, msg, duration = get_graphql_result(study_uid, kc)
                            graphql_pred_influx(orthanc_ip, cat, study_uid, patient_id, accession_number,
                                                script, vol, ai_result, duration, msg)
                        elif need_result == 'false':
                            logging.info("block:false")
                            queryresult, duration = graphql_prediction(study_uid, 'graphql', 'false', kc)
                            logging.info('query study uid [{0}], result is: {1}'.format(study_uid, queryresult))
                            logging.info('predict duration: {}'.format(duration))

        get_tc_perf()
        logging.info("[PASSED]Graphql prediction executed {0} * {1} = {2} times. "
                    .format(result_num, self.loop_time, result_num * self.loop_time))
        return True

        if not result_num > 0:
            fail_msg = "[FAILED]Can not find any study to predict. "
            logging.error(fail_msg)
            return False


if __name__ == '__main__':
    loadtest().sequence()