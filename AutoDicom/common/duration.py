# coding=utf-8

import logging
import datetime
from AutoDicom.common.queList import QueData, dicomSort
from AutoDicom.common.DicomSend import SendThread

from django.conf import settings
from AutoDicom.models import duration, dicom_group_detail

logger = logging.getLogger(__name__)  # 这里使用 __name__ 动态搜索定义的 logger 配置


def durationSend(ID):
    obj = duration.objects.get(id=ID)
    obj.start_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    obj.save()
    full_fn_fake = f'{settings.LOG_PATH}/{obj.type}{obj.id}'
    try:
        if obj.sendcount is None:
            count = int(dicom_group_detail.objects.filter(dicom_id__in=obj.dicom.split(",")).count())
        else:
            count = int(obj.sendcount)

        DicomList = dicomSort(obj.dicom.split(","), count)
        logger.info(f"DicomList:{len(DicomList)}")
    except Exception as e:
        logger.error(f"DicomList fail: {e}")
        return False
    try:
        que = QueData(
            relation_id=obj.id,
            Host_id=obj.Host_id,
            Type=obj.type,
            DicomList=DicomList,
            full_fn_fake=full_fn_fake,
            patientID=obj.patientid,
            patientName=obj.patientname
        )
    except Exception as e:
        logger.error(f"QueData fail: {e}")
        return False

    try:
        ST = SendThread(
            q=que,
            hostID=obj.Host_id,
            anonymous=True,
            full_fn_fake=full_fn_fake,
            sleepTime=obj.sleeptime,
            sleepCount=obj.sleepcount,
            stop=[1, ID]
        )
        ST.setDaemon(True)
        ST.start()
    except Exception as e:
        logger.error(f"SendThread fail: {e}")
        return False
    return True


def NormalSend(ID):
    obj = duration.objects.get(id=ID)
    full_fn_fake = f'{settings.LOG_PATH}/{obj.type}{obj.id}'
    try:
        DicomList = dicomSort(obj.dicom.split(","), obj.sendcount)
        logger.info(f"DicomList:{len(DicomList)}")
    except Exception as e:
        logger.error(f"DicomList fail: {e}")
    try:
        q = QueData(
            relation_id=obj.id,
            Host_id=obj.Host_id,
            Type=obj.type,
            DicomList=DicomList,
            full_fn_fake=full_fn_fake,
            patientID=obj.patientid,
            patientName=obj.patientname
        )
        logger.info(q)
    except Exception as e:
        logger.error(f"QueData fail: {e}")
    try:
        ST = SendThread(
            que=q,
            hostID=obj.Host_id,
            full_fn_fake=full_fn_fake,
        )
        ST.setDaemon(True)
        ST.start()
    except Exception as e:
        logger.error(f"SendThread fail: {e}")
        return False
    return True

