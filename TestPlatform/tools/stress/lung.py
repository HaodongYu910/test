from TestPlatform.common.regexUtil import *
from TestPlatform.utils.graphql.graphql_utils import GraphQLDriver



class lungtest():
    def __init__(self):
        self.kc = use_keycloak_bmutils("192.168.1.208", "biomind", "password")
        self.starttime ='2020-08-15 12:00:00'
        self.endtime='2020-08-15 23:59:59'

    def test(self):
        kc = use_keycloak_bmutils("192.168.1.208", "test", "Asd@123456")
        db_query ="select studyuid from prediction_metrics where modelname='lungct' and startpredictionts BETWEEN '" + self.starttime+ "'and'" +self.endtime +"';"
        result_db = connect_to_postgres('192.168.1.208',db_query)
        result_dict = result_db.to_dict(orient='records')
        dict={}
        for line in result_dict:
            graphql_query ='{ studies(StudyInstanceUID:"'+line["studyuid"]+'"){' \
		                      'Series{ '\
                                      'Instances{ SliceThickness } } } }'
            graphql = GraphQLDriver('/graphql',kc)
            results = graphql.execute_query(graphql_query)
            SliceThickness=round(float(results['studies'][0]['Series'][0]['Instances'][0]['SliceThickness']),2)
            if dict.get(SliceThickness) is None:
                dict[SliceThickness]='\''+str(line["studyuid"])+'\''
            else:
                a = dict[SliceThickness]
                dict[SliceThickness] = a+',\''+str(line["studyuid"])+'\''
        for key in dict:
            db_query ="select modelname, \
                        count(predid) as \"job_count\", \
                        cast(avg(predictionsec) as decimal(8,2)) as \"avg pred time /s \", \
                        percentile_disc(0.5) within group (order by predictionsec) as \"median pred time /s\",\
                        cast(min(predictionsec) as decimal(8,2)) as \"min pred time /s\", \
                        cast(max(predictionsec) as decimal(8,2)) as \"max pred time /s\",\
                        cast(stddev(predictionsec)/avg(predictionsec) as decimal(8,2)) as \"coef. of variation\" \
                        from prediction_metrics \
                        where endpredictionts BETWEEN '" + self.starttime+ "'and'" +self.endtime +"'and modelname = 'lungct' \
                        and studyuid in ("+dict[key] +") group by modelname\
                        order by min(startpredictionts);"
            result_db = connect_to_postgres('192.168.1.208', db_query)
            result_dict = result_db.to_dict(orient='records')


if __name__ == '__main__':
    lungtest().test()