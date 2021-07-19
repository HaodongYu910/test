# coding=utf-8
import pydicom
import logging
from ..common.dataSort import *

logger = logging.getLogger(__name__)  # 这里使用 __name__ 动态搜索定义的 logger 配置


def anonymization(**kwargs):

    """
    full_fn = dicom 数据路径
    rand_uid = 唯一值
    PatientID = 患者ID
    PatientName = 患者姓名
    full_fn_fake =匿名保存文件夹

    """
    full_fn = kwargs["full_fn"]
    full_fn_fake = kwargs["full_fn_fake"]
    rand_uid = kwargs["info"]["studyinstanceuid"]
    PatientID = kwargs["info"]["patientid"]
    PatientName = kwargs["info"]["patientname"]

    try:
        ds = pydicom.dcmread(full_fn, force=True)
    except Exception as e:
        logging.error('msg: failed to read file [{0}] error:{1}'.format(full_fn, e))
    # 匿名成新的数据
    try:
        ds.SeriesInstanceUID = norm_string(f'{ds.SeriesInstanceUID}.{rand_uid}', 64)
        ds.SOPInstanceUID = norm_string(f'{ds.SOPInstanceUID}.{rand_uid}', 64)
        ds.AccessionNumber = norm_string(f'{ds.AccessionNumber}.{rand_uid}', 16)
        ds.StudyInstanceUID = rand_uid
        ds.PatientID = PatientID
        ds.PatientName = PatientName

        ds.StudyDate = kwargs["info"]["cur_date"]
        ds.StudyTime = kwargs["info"]["cur_time"]
        ds.SeriesDate = kwargs["info"]["cur_date"]
        ds.SeriesTime = kwargs["info"]["cur_time"]
        # ds.ContentDate = cur_date
        # ds.ContentTime = cur_time
        # ds.AcquisitionDate = cur_date
        # ds.AcquisitionTime = cur_time
    except Exception as e:
        logging.error(
            'failed to anonymous :  error[{}]'.format(e))
    try:
        ds.save_as(full_fn_fake)
    except Exception as e:
        logging.error('errormsg: failed to save file [{0}] --{1}'.format(full_fn_fake, e))
