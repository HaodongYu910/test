import os
import re
import json
import time
import requests
import logging

logger = logging.getLogger(__name__)

class GraphQLDriver():
    def __init__(self, graphql_url, keycloakclient=None):
        self.graphql_url = graphql_url
        self.kc = keycloakclient

    def execute_query(self, query, timeout=600):
        if self.kc is not None:
            r = self.kc.post(
                url=self.graphql_url,
                timeout=timeout,
                verify=False,
                json={
                    'query': query
                }
            )
            if r is None:
                raise Exception('keycloakclient request canceled')
        else:
            r = requests.post(
                url=self.graphql_url,
                verify=False,
                headers={'Authorization': 'Basic Zm9vOmJhcg=='},
                timeout=timeout,
                json={
                    'query': query
                }
            )
        logger.info(r.json())
        if r.status_code == 200 and r.json()['data'] != None:
            return r.json()['data']
        return {}

    def pacs_query(self, dicomAE, query, timeout=600):
        '''
            Return the result of duration query
        '''
        # TestData = re.sub("\"(\w+)\":", r'\1:', json.dumps(query))
        data = self.convert_to_graphql_syntax(query)
        query_data = str(
            '{query(dicomAE:"' + str(dicomAE) + '" query: ' + data + ')}'
        )
        return self.execute_query(query_data, timeout)

    def graphql_query(self, query, timeout=600):
        '''
            Return the result of graphql query
        '''
        return self.execute_query(query, timeout)

    def convert_to_graphql_syntax(self, payload):
        '''
            Return the result of graphql query
        '''
        return re.sub("\"(\w+)\":", r'\1:',json.dumps(payload))

    def post_to_db(self, prediction, study_uid, index):
        gql='mutation{{hanalyticsData(index:\"{}\" value:\"{}\" studyUID:\"{}\")}}'.format(index, json.dumps(prediction).replace('\"', '\\\"'), study_uid)
        return self.execute_query(gql)

    def get_archive_url(self, dicomAE, level, uid):
        '''
            Return the URL for download study or series
        '''
        if level is 'study':
            query = '{{studies(dicomAE:"{}" StudyInstanceUID:"{}"){{Archive}}}}'.format(
                dicomAE, uid)
        elif level is 'series':
            query = '{{series(dicomAE:"{}" SeriesInstanceUID:"{}"){{Archive}}}}'.format(
                dicomAE, uid)
        else:
            return None
        return self.execute_query(query)

    def get_media_url(self, level, uid, dicomAE=''):  # dicomAE='dicomAE: "orthanc"'
        '''
            Return the URL for download study or series
        '''
        if level is 'study':
            query = '{{studies({} StudyInstanceUID:"{}"){{Media}}}}'.format(
                dicomAE, uid)
        elif level is 'series':
            query = '{{studies({} StudyInstanceUID:"{}"){{Series{{Media}}}}}}'.format(
                dicomAE, uid)
        else:
            return None
        return self.execute_query(query)

    def get_all_reports(self, dicomAE, StudyInstanceUID):
        '''
            Return a list of all reports for the study
        '''
        query = '{{reports(dicomAE:"{}" StudyInstanceUID:"{}") {{ \
                    report_title  description  diagnosis  submit_by  verify_by  complete  verify \
                    submit_date submit_time approval_time SOPInstanceUID InstanceCreationDate \
                    InstanceCreationTime ReferringPhysicianName HanalyticsReports \
                }}}}'.format(dicomAE, StudyInstanceUID)
        return self.execute_query(query)

    def get_all_annotations(self, dicomAE, StudyInstanceUID):
        '''
            Return a list of all annotations for the study
        '''
        query = '{{annotations(dicomAE:"{}" StudyInstanceUID:"{}") {{ \
                    images labels SOPInstanceUID InstanceCreationDate InstanceCreationTime ReferringPhysicianName\
                }}}}'.format(dicomAE, StudyInstanceUID)
        return self.execute_query(query)

    def get_all_protocols(self, dicomAE, StudyInstanceUID):
        '''
            Return a list of all protocols for the study
        '''
        query = '{{protocols(dicomAE:"{}" StudyInstanceUID:"{}") {{ \
                    pprediction preport pprediction_description pmodels pseries_classifier pdicom_folder pstudy_uid \
                    pseries pmetadata SOPInstanceUID InstanceCreationDate InstanceCreationTime \
                }}}}'.format(dicomAE, StudyInstanceUID)
        return self.execute_query(query)

    def get_latest_report(self, dicomAE, StudyInstanceUID, timeout=120):
        '''
            Return the lastest report of the study
        '''
        query = '{{studies(dicomAE:"{}" StudyInstanceUID:"{}"){{LatestReport}}}}'.format(
            dicomAE, StudyInstanceUID)
        return self.execute_query(query, timeout)

    def get_latest_annotation(self, dicomAE, StudyInstanceUID, timeout=120):
        '''
            Return the lastest annotation of the study
        '''
        query = '{{studies(dicomAE:"{}" StudyInstanceUID:"{}"){{LatestAnnotation}}}}'.format(
            dicomAE, StudyInstanceUID)
        return self.execute_query(query, timeout)

    def get_latest_protocol(self, dicomAE, StudyInstanceUID, timeout=120):
        '''
            Return the lastest protocol of the study
        '''
        query = '{{studies(dicomAE:"{}" StudyInstanceUID:"{}"){{LatestProtocol}}}}'.format(
            dicomAE, StudyInstanceUID)
        return self.execute_query(query, timeout)

