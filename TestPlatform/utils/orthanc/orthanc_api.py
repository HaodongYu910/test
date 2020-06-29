import json
import os
import traceback

from common_utils import utils
from common_utils.config.config import CONFIG
from engine3d_log import logger


@logger.catch
def download_dcm_zip_for_series(kc, series_id):
    '''
    Call the API to get the dcm image 调用API获取dcm图像
    :param kc: KeycloakClient (type: object)
    :param series_id: orthanc series public id
    :return: dcm zip data
    '''
    try:
        content = kc.get("/orthanc/series/{0}/archive".format(
            series_id), timeout=CONFIG.orthanc_timeout, verify=False).content
    except Exception as e:
        logger.error(
            'failed to download image from series_id, error:[{0}]'.format(e))
        return None, 'orthanc_001'
    return content, None


@logger.catch
def get_series_id_by_series_uid(kc, series_uid):
    '''
    Get series id by series uid 通过series uid获取series id
    :param kc: KeycloakClient (type: object)
    :param series_uid: orthanc series instance uid
    :returns: orthanc series public id and msg_code
    '''
    json_data = {
        "Level": "Series",
        "Query": {"SeriesInstanceUID": series_uid}
    }
    try:
        res = kc.post(
            "/orthanc/tools/find",
            json=json_data,
            timeout=CONFIG.orthanc_timeout,
            verify=False)
        data = json.loads(res.content) if res else None
        if not data:
            return [], 'orthanc_003'
    except Exception as e:
        logger.error(
            'get series_id ERROR, error[{0}]\n{1}'.format(
                e, traceback.format_exc()))
        return None, 'orthanc_002'
    try:
        series_id = data[0]
    except Exception as e:
        logger.error('data:{0}'.format(data))
        logger.error(
            'orthanc find series_id error:[{0}]\n{1}'.format(
                e, traceback.format_exc()))
        return None, 'orthanc_004'
    return series_id, None
