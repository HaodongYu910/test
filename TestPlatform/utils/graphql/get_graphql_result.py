import operator,logging
from TestPlatform.utils.graphql.graphql_prediction_series import graphql_prediction_series
from TestPlatform.utils.graphql.graphql_ai_status import graphql_ai_status

def get_graphql_result(study_uid,series,kc):
    cat = 'default_none'
    vol = float(0)
    ai_result = []
    msg = 'default_none'
    mask_list = 'default_none'
    queryresult, duration = \
        graphql_prediction_series(study_uid, series, 'graphql','true',kc)

    logging.info('query study uid [{0}], result is: {1}'.format(study_uid, queryresult))
    logging.info('predict duration: {}'.format(duration))

    if not isinstance(queryresult, dict) or len(queryresult) == 0:
        msg = "Graphql prediction failed: {0}".format(queryresult)
        logging.error(msg)
        return mask_list, cat, vol, ai_result, queryresult, duration

    clas_dict = {}
    mask_list = {}
    print(type(queryresult["ai_biomind"]))
    if queryresult["ai_biomind"] is not None:
    # if study_uid == queryresult["ai_biomind"]['pstudy_uid']:
        if len(queryresult['ai_biomind']['preport']) != 0:
            if queryresult['ai_biomind']['pprediction'] is not None:
                predictions = queryresult['ai_biomind']['pprediction']
                # get disease content
                for volumeID, predictionList in predictions.items():
                    for predictionItem in predictionList:
                        # del predictionItem['mask']
                        # if 'disease' is in category, this study has disease
                        if 'disease' in predictionItem['category']:
                            cat = predictionItem['category'].split('.')[0]
                            clas = predictionItem['classification']
                            clas_dict.update(clas)
                            mask_dict = {}
                            mask = predictionItem['mask']
                            mask_dict[list(clas.keys())[0]] = mask
                            mask_list.update(mask_dict)
                            vol = float(predictionItem['volume'])
                            logging.info("clas_dict: {}".format(clas_dict))
                sorted_clas_dict = sorted(clas_dict.items(), key=operator.itemgetter(1), reverse=True)

                # has disease
                if len(sorted_clas_dict) != 0:
                    ai_result = sorted_clas_dict
                    msg = "Finished graphql query successfully, found disease. Study UID = {0} ".format(study_uid)
                    logging.info(msg)
                # clas_dict={}, no disease
                else:
                    ai_status_result = graphql_ai_status(study_uid, 'graphql',kc)
                    logging.info('ai_status_result: {}'.format(ai_status_result))
                    for ai_status in ai_status_result["studyView"]:
                        if ai_status['aistatus'] == 1:
                            ai_result = ['no_disease']
                            msg = "Finished graphql query successfully, and no disease found in the study. Study UID = {0} ".format(study_uid)
                            logging.info(msg)
                        else:
                            ai_result = sorted_clas_dict
                            msg = "Finished graphql query successfully, but failed to get result. Study UID = {0} ".format(study_uid)
                            logging.info(msg)
                logging.info('ai_result: {}'.format(ai_result))
                # for CT Lung classification result
                pclassification = queryresult['ai_biomind']['pclassification']
                if pclassification is not None:
                    ai_result = pclassification
            else:
                msg = 'Got no pprediction.'
                logging.error(msg)
        else:
            msg = "No series matched the model requirements. Study UID = {0} ".format(study_uid)
            msg = "No preports.".format(study_uid)
            logging.error(msg)
    else:
        msg = "Study UID is not correct or no prediction. Study UID = {0} ".format(study_uid)
        logging.error(msg)
    return mask_list, cat, vol, ai_result, msg, duration
